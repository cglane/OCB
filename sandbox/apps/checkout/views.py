import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from oscar.apps.checkout import views
from django.contrib.auth import login
from django.utils.http import urlquote
from django.conf import settings
from django import http
from django.utils.translation import ugettext as _
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy

from oscar.apps.payment import forms, models
from oscar.core.loading import get_class, get_classes, get_model
from oscar.apps.checkout import signals
from oscar.core.compat import user_is_authenticated
from django.shortcuts import redirect
from django.utils import six
from django.core.files.storage import FileSystemStorage
import stripe
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
GatewayForm = get_class('checkout.forms', 'GatewayForm')
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY")

UserAddress = get_model('address', 'UserAddress')
UnableToPlaceOrder = get_class('order.exceptions', 'UnableToPlaceOrder')
RedirectRequired, UnableToTakePayment, PaymentError \
    = get_classes('payment.exceptions', ['RedirectRequired',
                                         'UnableToTakePayment',
                                         'PaymentError'])
OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')
logger = logging.getLogger('oscar.checkout')



class IndexView(CheckoutSessionMixin, generic.FormView):
    """
    First page of the checkout.  We prompt user to either sign in, or
    to proceed as a guest (where we still collect their email address).
    """
    template_name = 'checkout/gateway.html'
    form_class = GatewayForm
    success_url = reverse_lazy('checkout:shipping-address')
    pre_conditions = [
        'check_basket_is_not_empty',
        'check_basket_is_valid']

    def post(self, request,  *args, **kwargs):
        if request.FILES and request.FILES.get('resaleCertificate'):
            myfile = request.FILES['resaleCertificate']
            filename = request.basket.resale_certificate.save(myfile.name, myfile)
        return super(IndexView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # We redirect immediately to shipping address stage if the user is
        # signed in.
        if user_is_authenticated(request.user):
            # We raise a signal to indicate that the user has entered the
            # checkout process so analytics tools can track this event.
            signals.start_checkout.send_robust(
                sender=self, request=request)
            return self.get_success_response()
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(IndexView, self).get_form_kwargs()
        email = self.checkout_session.get_guest_email()
        if email:
            kwargs['initial'] = {
                'username': email,
            }
        return kwargs

    def form_valid(self, form):
        if form.is_guest_checkout() or form.is_new_account_checkout():
            email = form.cleaned_data['username']
            self.checkout_session.set_guest_email(email)

            # We raise a signal to indicate that the user has entered the
            # checkout process by specifying an email address.
            signals.start_checkout.send_robust(
                sender=self, request=self.request, email=email)

            if form.is_new_account_checkout():
                messages.info(
                    self.request,
                    _("Create your account and then you will be redirected "
                      "back to the checkout process"))
                self.success_url = "%s?next=%s&email=%s" % (
                    reverse('customer:register'),
                    reverse('checkout:shipping-address'),
                    urlquote(email)
                )
        else:
            user = form.get_user()
            login(self.request, user)

            # We raise a signal to indicate that the user has entered the
            # checkout process.
            signals.start_checkout.send_robust(
                sender=self, request=self.request)
        return redirect(self.get_success_url())

    def get_success_response(self):
        return redirect(self.get_success_url())


class PaymentDetailsView(OrderPlacementMixin, generic.TemplateView):
    """
    For taking the details of payment and creating the order.

    This view class is used by two separate URLs: 'payment-details' and
    'preview'. The `preview` class attribute is used to distinguish which is
    being used. Chronologically, `payment-details` (preview=False) comes before
    `preview` (preview=True).

    If sensitive details are required (eg a bankcard), then the payment details
    view should submit to the preview URL and a custom implementation of
    `validate_payment_submission` should be provided.

    - If the form data is valid, then the preview template can be rendered with
      the payment-details forms re-rendered within a hidden div so they can be
      re-submitted when the 'place order' button is clicked. This avoids having
      to write sensitive data to disk anywhere during the process. This can be
      done by calling `render_preview`, passing in the extra template context
      vars.

    - If the form data is invalid, then the payment details templates needs to
      be re-rendered with the relevant error messages. This can be done by
      calling `render_payment_details`, passing in the form instances to pass
      to the templates.

    The class is deliberately split into fine-grained methods, responsible for
    only one thing.  This is to make it easier to subclass and override just
    one component of functionality.

    All projects will need to subclass and customise this class as no payment
    is taken by default.
    """
    template_name = 'checkout/payment_details.html'
    template_name_preview = 'checkout/preview.html'
    # These conditions are extended at runtime depending on whether we are in
    # 'preview' mode or not.
    pre_conditions = [
        'check_basket_is_not_empty',
        'check_basket_is_valid',
        'check_user_email_is_captured',
        'check_shipping_data_is_captured']
    pre_conditions = []

    # If preview=True, then we render a preview template that shows all order
    # details ready for submission.
    preview = False
    def get_context_data(self, **kwargs):
        kwargs = super(PaymentDetailsView, self).get_context_data(**kwargs)
        kwargs['stripe_key'] =  getattr(settings, 'STRIPE_PUBLIC_KEY')
        kwargs['total'] = int(float(kwargs['order_total'].incl_tax) * 100.0)
        return kwargs

    def handle_payment(self,  order_number, total, **kwargs):
        # Talk to payment gateway.  If unsuccessful/error, raise a
        # PaymentError exception which we allow to percolate up to be caught
        # and handled by the core PaymentDetailsView.
        # reference = gateway.pre_auth(order_number, total.incl_tax, kwargs['bankcard'])
        # Payment successful! Record payment source


        reference = self.stripe_capture()
        source_type, __ = models.SourceType.objects.get_or_create(
            name="Stripe")
        source = models.Source(
            source_type=source_type,
            amount_allocated=total.incl_tax,
            reference=reference.id)
        self.add_payment_source(source)

        # Record payment event
        self.add_payment_event('pre-auth', total.incl_tax)
    def stripe_capture(self):
        self.token = self.request.session['token']
        self.stripe_key =  getattr(settings, 'STRIPE_PUBLIC_KEY')
        self.capture_id = self.request.session['charge_id']
        try:
            charge = stripe.Charge.retrieve(self.capture_id)
            response = charge.capture()
            return response
        except stripe.error.CardError as e:
            pass
    def stripe_authorize(self, *args, **kwargs):
        self.token = self.request.POST.get("stripeToken")
        self.request.session['token'] = self.token
        ctx = self.get_context_data(**kwargs)
        ## amount
        try:
            charge = stripe.Charge.create(
                amount=ctx['total'],
                currency="usd",
                source=self.token,
                capture=False,
                description="The product charged to the user",
            )
            self.request.session['charge_id'] = charge.id
            return charge
        except stripe.error.CardError as e:

            body = e.json_body
            err = body.get('error', {})

            print ("Status is: %s" % e.http_status)
            print ("Type is: %s" % err.get('type'))
            print ("Code is: %s" % err.get('code'))
            # param is '' in this case
            print ("Param is: %s" % err.get('param'))
            print ("Message is: %s" % err.get('message'))

        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            pass
        except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
            pass
        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            pass
        except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
            pass
        except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            pass
        except Exception as e:
        # Something else happened, completely unrelated to Stripe
            pass
    def post(self, request, *args, **kwargs):
        # Posting to payment-details isn't the right thing to do.  Form
        # submissions should use the preview URL.
        # We use a custom parameter to indicate if this is an attempt to place
        # an order (normally from the preview page).  Without this, we assume a
        # payment form is being submitted from the payment details view. In
        # this case, the form needs validating and the order preview shown.
        # Posting to payment-details isn't the right thing to do.  Form
        # submissions should use the preview URL.
        # if not self.preview:
        #     return http.HttpResponseBadRequest()
        # We use a custom parameter to indicate if this is an attempt to place
        # an order (normally from the preview page).  Without this, we assume a
        # payment form is being submitted from the payment details view. In
        # this case, the form needs validating and the order preview shown.
        if request.POST.get('action', '') == 'place_order':
            return self.handle_place_order_submission(request)
        return self.handle_payment_details_submission(request)


    def handle_place_order_submission(self, request):
        """
        Handle a request to place an order.

        This method is normally called after the customer has clicked "place
        order" on the preview page. It's responsible for (re-)validating any
        form information then building the submission dict to pass to the
        `submit` method.

        If forms are submitted on your payment details view, you should
        override this method to ensure they are valid before extracting their
        data into the submission dict and passing it onto `submit`.
        """
        return self.submit(**self.build_submission())

    def handle_payment_details_submission(self, request):
        """
        Handle a request to submit payment details.

        This method will need to be overridden by projects that require forms
        to be submitted on the payment details view.  The new version of this
        method should validate the submitted form data and:

        - If the form data is valid, show the preview view with the forms
          re-rendered in the page
        - If the form data is invalid, show the payment details view with
          the form errors showing.

        """
        # No form data to validate by default, so we simply render the preview
        # page.  If validating form data and it's invalid, then call the
        # render_payment_details view.
        stripe_response = self.stripe_authorize()
        if stripe_response:
            return self.render_preview(request)

    def render_preview(self, request, **kwargs):
        """
        Show a preview of the order.

        If sensitive data was submitted on the payment details page, you will
        need to pass it back to the view here so it can be stored in hidden
        form inputs.  This avoids ever writing the sensitive data to disk.
        """
        self.preview = True
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)

    def render_payment_details(self, request, **kwargs):
        """
        Show the payment details page

        This method is useful if the submission from the payment details view
        is invalid and needs to be re-rendered with form errors showing.
        """
        self.preview = False
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)

    def get_default_billing_address(self):
        """
        Return default billing address for user

        This is useful when the payment details view includes a billing address
        form - you can use this helper method to prepopulate the form.

        Note, this isn't used in core oscar as there is no billing address form
        by default.
        """
        if not user_is_authenticated(self.request.user):
            return None
        try:
            return self.request.user.addresses.get(is_default_for_billing=True)
        except UserAddress.DoesNotExist:
            return None

    def submit(self, user, basket, shipping_address, shipping_method,  # noqa (too complex (10))
               shipping_charge, billing_address, order_total,
               payment_kwargs=None, order_kwargs=None):

        """
        Submit a basket for order placement.

        The process runs as follows:

         * Generate an order number
         * Freeze the basket so it cannot be modified any more (important when
           redirecting the user to another site for payment as it prevents the
           basket being manipulated during the payment process).
         * Attempt to take payment for the order
           - If payment is successful, place the order
           - If a redirect is required (eg PayPal, 3DSecure), redirect
           - If payment is unsuccessful, show an appropriate error message

        :basket: The basket to submit.
        :payment_kwargs: Additional kwargs to pass to the handle_payment
                         method. It normally makes sense to pass form
                         instances (rather than model instances) so that the
                         forms can be re-rendered correctly if payment fails.
        :order_kwargs: Additional kwargs to pass to the place_order method
        """
        if payment_kwargs is None:
            payment_kwargs = {}
        if order_kwargs is None:
            order_kwargs = {}

        # Taxes must be known at this point
        assert basket.is_tax_known, (
            "Basket tax must be set before a user can place an order")
        assert shipping_charge.is_tax_known, (
            "Shipping charge tax must be set before a user can place an order")

        # We generate the order number first as this will be used
        # in payment requests (ie before the order model has been
        # created).  We also save it in the session for multi-stage
        # checkouts (eg where we redirect to a 3rd party site and place
        # the order on a different request).
        order_number = self.generate_order_number(basket)
        self.checkout_session.set_order_number(order_number)
        logger.info("Order #%s: beginning submission process for basket #%d",
                    order_number, basket.id)

        # Freeze the basket so it cannot be manipulated while the customer is
        # completing payment on a 3rd party site.  Also, store a reference to
        # the basket in the session so that we know which basket to thaw if we
        # get an unsuccessful payment response when redirecting to a 3rd party
        # site.
        self.freeze_basket(basket)
        self.checkout_session.set_submitted_basket(basket)

        # We define a general error message for when an unanticipated payment
        # error occurs.
        error_msg = _("A problem occurred while processing payment for this "
                      "order - no payment has been taken.  Please "
                      "contact customer services if this problem persists")

        signals.pre_payment.send_robust(sender=self, view=self)

        try:
            self.handle_payment( order_number, order_total, **payment_kwargs)
        except RedirectRequired as e:
            # Redirect required (eg PayPal, 3DS)
            logger.info("Order #%s: redirecting to %s", order_number, e.url)
            return http.HttpResponseRedirect(e.url)
        except UnableToTakePayment as e:
            # Something went wrong with payment but in an anticipated way.  Eg
            # their bankcard has expired, wrong card number - that kind of
            # thing. This type of exception is supposed to set a friendly error
            # message that makes sense to the customer.
            msg = six.text_type(e)
            logger.warning(
                "Order #%s: unable to take payment (%s) - restoring basket",
                order_number, msg)
            self.restore_frozen_basket()

            # We assume that the details submitted on the payment details view
            # were invalid (eg expired bankcard).
            return self.render_payment_details(
                self.request, error=msg, **payment_kwargs)
        except PaymentError as e:
            # A general payment error - Something went wrong which wasn't
            # anticipated.  Eg, the payment gateway is down (it happens), your
            # credentials are wrong - that king of thing.
            # It makes sense to configure the checkout logger to
            # mail admins on an error as this issue warrants some further
            # investigation.
            msg = six.text_type(e)
            logger.error("Order #%s: payment error (%s)", order_number, msg,
                         exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=error_msg, **payment_kwargs)
        except Exception as e:
            # Unhandled exception - hopefully, you will only ever see this in
            # development...
            logger.error(
                "Order #%s: unhandled exception while taking payment (%s)",
                order_number, e, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=error_msg, **payment_kwargs)

        signals.post_payment.send_robust(sender=self, view=self)

        # If all is ok with payment, try and place order
        logger.info("Order #%s: payment successful, placing order",
                    order_number)
        try:
            return self.handle_order_placement(
                order_number, user, basket, shipping_address, shipping_method,
                shipping_charge, billing_address, order_total, **order_kwargs)
        except UnableToPlaceOrder as e:
            # It's possible that something will go wrong while trying to
            # actually place an order.  Not a good situation to be in as a
            # payment transaction may already have taken place, but needs
            # to be handled gracefully.
            msg = six.text_type(e)
            logger.error("Order #%s: unable to place order - %s",
                         order_number, msg, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=msg, **payment_kwargs)

    def get_template_names(self):
        return [self.template_name_preview] if self.preview else [
            self.template_name]

