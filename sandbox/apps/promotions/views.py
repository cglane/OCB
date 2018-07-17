from django.core.urlresolvers import reverse
from oscar.core.loading import get_model
from django.views.generic import RedirectView, TemplateView
from django.conf import settings
AttributeOptionGroup = get_model('catalogue', 'AttributeOptionGroup')
Products = get_model('catalogue', 'Product')
ProductImages = get_model('catalogue', 'ProductImage')
from django.contrib import messages
from django.core.paginator import InvalidPage
from django.shortcuts import get_object_or_404, redirect

class FabricOptionsView(TemplateView):
    template_name = 'partials/fabric_options.html'
    def get_context_data(self, **kwargs):
        ctx = super(FabricOptionsView, self).get_context_data(**kwargs)
        fabric_options_list = []
        options_groups = AttributeOptionGroup.objects.filter(name__icontains="fabrics").exclude(name__icontains="piping")
        for group in options_groups:
            local_dict = {'name': group.name, 'options': group.options.all()}
            fabric_options_list.append(local_dict)
        ctx['fabric_options'] = fabric_options_list
        return ctx

class HomeView(TemplateView):
    """
    This is the home page and will typically live at /
    """
    template_name = 'promotions/home-extends.html'
    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx['images'] = getattr(settings,'LANDING_PAGE_IMAGES')
        ctx['main_image'] = getattr(settings,'LANDING_PAGE_MAIN_IMAGE')
        ctx['fabric_options'] = getattr(settings, 'LANDING_PAGE_FABRIC_OPTIONS')
        ctx['bedswing_options'] = getattr(settings, 'LANDING_PAGE_BEDSWING_OPTIONS')
        return ctx


class AboutPageView(TemplateView):
    template_name =  'promotions/about.html'
    def get_context_data(self, **kwargs):
        ctx = super(AboutPageView, self).get_context_data(**kwargs)
        ctx['image'] = getattr(settings, 'ABOUT_PAGE_IMAGE')
        return ctx

class FaqPageView(TemplateView):
    template_name = 'promotions/faqs.html'

class RecordClickView(RedirectView):
    """
    Simple RedirectView that helps recording clicks made on promotions
    """
    permanent = False
    model = None

    def get_redirect_url(self, **kwargs):
        try:
            prom = self.model.objects.get(pk=kwargs['pk'])
        except self.model.DoesNotExist:
            return reverse('promotions:home')

        if prom.promotion.has_link:
            prom.record_click()
            return prom.link_url
        return reverse('promotions:home')
