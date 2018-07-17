from django import forms
from django.conf import settings
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from oscar.core.loading import get_model
from django.utils.encoding import smart_text as smart_unicode
from django.utils.encoding import force_str, force_text
from django.forms.utils import flatatt

from oscar.forms import widgets

Line = get_model('basket', 'line')
Basket = get_model('basket', 'basket')
Product = get_model('catalogue', 'product')
AttributeOptionGroup = get_model('catalogue', 'attributeOptionGroup' )


class GroupedSelect(forms.Select): 
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = '' 
        final_attrs = self.build_attrs(attrs) 
        final_attrs['class'] = 'option-select-class form-control'
        final_attrs['name'] = name
        output = [u'<select  %s>' % flatatt(final_attrs)] 
        for group_label, group in self.choices: 
            if group_label:
                group_label = smart_unicode(group_label) 
            option_value = smart_unicode(group[0])
            option_label = smart_unicode(group[1]) 
            output.append(u'<option value="%s"image="%s">%s</option>' % (escape(option_value), escape(group_label), escape(option_label)))  
        output.append(u'</select>') 
        return u'\n'.join(output)

# field for grouped choices, handles cleaning of funky choice tuple
class GroupedChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), required=False, widget=GroupedSelect, label=None, initial=None, help_text=None):
        super(forms.ChoiceField, self).__init__(required, widget, label, initial, help_text)
        self.choices = choices
        
    def clean(self, value):
        """
        Validates that the input is in self.choices.
        """
        value = super(forms.ChoiceField, self).clean(value)
        if value in (None, ''):
            value = u''
        value = smart_unicode(value)
        if value == u'':
         return value
        valid_values = []
        for group_label, group in self.choices:
            valid_values += [x.encode("utf8") for x in group]
        if str(value).encode("utf8") not in valid_values:
            raise forms.ValidationError(u'Select a valid choice. That choice is not one of the available choices.')
        return value
    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        text_value = force_text(value)
        for group_label, group in self.choices:
            if isinstance(group, (list, tuple)):
                # This is an optgroup, so look inside the group for options
                if value == group[0] or text_value == force_text(group[1]):
                        return True
            else:
                if value == k or text_value == force_text(k):
                    return True
        return False

class BasketLineForm(forms.ModelForm):
    save_for_later = forms.BooleanField(
        initial=False, required=False, label=_('Save for Later'))

    def __init__(self, strategy, *args, **kwargs):
        super(BasketLineForm, self).__init__(*args, **kwargs)
        self.instance.strategy = strategy

    def clean_quantity(self):
        qty = self.cleaned_data['quantity']
        if qty > 0:
            self.check_max_allowed_quantity(qty)
            self.check_permission(qty)
        return qty

    def check_max_allowed_quantity(self, qty):
        # Since `Basket.is_quantity_allowed` checks quantity of added product
        # against total number of the products in the basket, instead of sending
        # updated quantity of the product, we send difference between current
        # number and updated. Thus, product already in the basket and we don't
        # add second time, just updating number of items.
        qty_delta = qty - self.instance.quantity
        is_allowed, reason = self.instance.basket.is_quantity_allowed(qty_delta)
        if not is_allowed:
            raise forms.ValidationError(reason)

    def check_permission(self, qty):
        policy = self.instance.purchase_info.availability
        is_available, reason = policy.is_purchase_permitted(
            quantity=qty)
        if not is_available:
            raise forms.ValidationError(reason)

    class Meta:
        model = Line
        fields = ['quantity']


class SavedLineForm(forms.ModelForm):
    move_to_basket = forms.BooleanField(initial=False, required=False,
                                        label=_('Move to Basket'))

    class Meta:
        model = Line
        fields = ('id', 'move_to_basket')

    def __init__(self, strategy, basket, *args, **kwargs):
        self.strategy = strategy
        self.basket = basket
        super(SavedLineForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SavedLineForm, self).clean()
        if not cleaned_data['move_to_basket']:
            # skip further validation (see issue #666)
            return cleaned_data

        # Get total quantity of all lines with this product (there's normally
        # only one but there can be more if you allow product options).
        lines = self.basket.lines.filter(product=self.instance.product)
        current_qty = lines.aggregate(Sum('quantity'))['quantity__sum'] or 0
        desired_qty = current_qty + self.instance.quantity

        result = self.strategy.fetch_for_product(self.instance.product)
        is_available, reason = result.availability.is_purchase_permitted(
            quantity=desired_qty)
        if not is_available:
            raise forms.ValidationError(reason)
        return cleaned_data


class BasketVoucherForm(forms.Form):
    code = forms.CharField(max_length=128, label=_('Code'))

    def __init__(self, *args, **kwargs):
        super(BasketVoucherForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()


class AddToBasketForm(forms.Form):
    quantity = forms.IntegerField(initial=1, min_value=1, label=_('Quantity'))

    def __init__(self, basket, product, *args, **kwargs):
        # Note, the product passed in here isn't necessarily the product being
        # added to the basket. For child products, it is the *parent* product
        # that gets passed to the form. An optional product_id param is passed
        # to indicate the ID of the child product being added to the basket.
        self.basket = basket
        self.parent_product = product

        super(AddToBasketForm, self).__init__(*args, **kwargs)

        # Dynamically build fields
        if product.is_parent:
            self._create_parent_product_fields(product)
        self._create_product_fields(product)

    # Dynamic form building methods

    def _create_parent_product_fields(self, product):
        """
        Adds the fields for a "group"-type product (eg, a parent product with a
        list of children.

        Currently requires that a stock record exists for the children
        """
        choices = []
        colors = [(x.id, x.title) for x in product.colors.all()]
        disabled_values = []
        for child in product.children.all():
            # Build a description of the child, including any pertinent
            # attributes
            attr_summary = child.attribute_summary
            if attr_summary:
                summary = attr_summary
            else:
                summary = child.get_title()

            # Check if it is available to buy
            info = self.basket.strategy.fetch_for_product(child)
            if not info.availability.is_available_to_buy:
                disabled_values.append(child.id)

            choices.append((child.id, summary))
        self.fields['child_ids'] = forms.ChoiceField(
            choices=tuple(choices), label="Options",
            widget=widgets.AdvancedSelect(disabled_values=disabled_values))
        ### Add Colors option if it exits
        if colors:
            self.fields['color_ids'] = forms.ChoiceField(
                choices=colors, label="Colors"
            )
    def _create_product_fields(self, product):
        """
        I am finding product types and mapping them to the option 
        groups tied to the product class.
        This will create a Select element on the product view page.
        If there is no option group it will display as a simple input.        
        """
        attribute_option_groups = AttributeOptionGroup.objects.all()
        for option in product.product_options.all():
            local_attribute_value = [x for x in attribute_option_groups if x.name == option.name]
            if(local_attribute_value):
                choices = []
                local_attribute_options = local_attribute_value[0].options.all()
                for attribute_option in local_attribute_options:
                    if attribute_option.image:
                     choices.append((attribute_option.image.url,(attribute_option.option, attribute_option.option)))
                    else:
                        choices.append(('',(attribute_option.option, attribute_option.option)))
                options_list = GroupedChoiceField(choices=choices, label=option.name)
                self.fields[option.code] = options_list
            else:
                self.fields[option.code] = forms.CharField(
                    label=option.name, required=option.is_required)

    # Cleaning

    def clean_child_id(self):
        try:
            child = self.parent_product.children.get(
                id=self.cleaned_data['child_id'])
        except Product.DoesNotExist:
            raise forms.ValidationError(
                _("Please select a valid product"))

        # To avoid duplicate SQL queries, we cache a copy of the loaded child
        # product as we're going to need it later.
        self.child_product = child

        return self.cleaned_data['child_id']

    def clean_quantity(self):
        # Check that the proposed new line quantity is sensible
        qty = self.cleaned_data['quantity']
        basket_threshold = settings.OSCAR_MAX_BASKET_QUANTITY_THRESHOLD
        if basket_threshold:
            total_basket_quantity = self.basket.num_items
            max_allowed = basket_threshold - total_basket_quantity
            if qty > max_allowed:
                raise forms.ValidationError(
                    _("Due to technical limitations we are not able to ship"
                      " more than %(threshold)d items in one order. Your"
                      " basket currently has %(basket)d items.")
                    % {'threshold': basket_threshold,
                       'basket': total_basket_quantity})
        return qty

    @property
    def product(self):
        """
        The actual product being added to the basket
        """
        # Note, the child product attribute is saved in the clean_child_id
        # method
        return getattr(self, 'child_product', self.parent_product)

    def clean(self):
        info = self.basket.strategy.fetch_for_product(self.product)

        # Check currencies are sensible
        if (self.basket.currency and
                info.price.currency != self.basket.currency):
            raise forms.ValidationError(
                _("This product cannot be added to the basket as its currency "
                  "isn't the same as other products in your basket"))

        # Check user has permission to add the desired quantity to their
        # basket.
        current_qty = self.basket.product_quantity(self.product)
        desired_qty = current_qty + self.cleaned_data.get('quantity', 1)
        is_permitted, reason = info.availability.is_purchase_permitted(
            desired_qty)
        if not is_permitted:
            raise forms.ValidationError(reason)

        return self.cleaned_data

    # Helpers

    def cleaned_options(self):
        """
        Return submitted options in a clean format
        """
        options = []
        for option in self.parent_product.options:
            if option.code in self.cleaned_data:
                options.append({
                    'option': option,
                    'value': self.cleaned_data[option.code]})
        return options


class SimpleAddToBasketForm(AddToBasketForm):
    """
    Simplified version of the add to basket form where the quantity is
    defaulted to 1 and rendered in a hidden widget

    Most of the time, you won't need to override this class. Just change
    AddToBasketForm to change behaviour in both forms at once.
    """

    def __init__(self, *args, **kwargs):
        super(SimpleAddToBasketForm, self).__init__(*args, **kwargs)
        if 'quantity' in self.fields:
            self.fields['quantity'].initial = 1
            self.fields['quantity'].widget = forms.HiddenInput()
