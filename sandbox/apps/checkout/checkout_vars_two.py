from django.conf import settings


def checkout(request):
    show_tax_separately \
        = getattr(settings, 'SHOW_TAX_CHECKOUT', False)
    return {'show_tax_separately': show_tax_separately}