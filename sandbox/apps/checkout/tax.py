from decimal import Decimal as D
from django.conf import settings
def apply_to(submission):

    tax_rate = getattr(settings, 'SALES_TAX')
    STATE_TAX_RATES = {
        'SC': D(tax_rate)
    }
    shipping_address = submission['shipping_address']
    rate = STATE_TAX_RATES.get(
        shipping_address.state.upper(), D('0.00'))
        
    ##If the basket has a resale certificate uploaded then that person will not pay tax
    if submission['basket'].resale_certificate:
        rate = D('0.00')

    for line in submission['basket'].all_lines():
        line_tax = calculate_tax(
            line.line_price_excl_tax_incl_discounts, rate)
        unit_tax = (line_tax / line.quantity).quantize(D('0.01'))
        line.purchase_info.price.tax = unit_tax

    # Note, we change the submission in place - we don't need to
    # return anything from this function
    shipping_charge = submission['shipping_charge']
    if shipping_charge is not None:
        shipping_charge.tax = calculate_tax(
            shipping_charge.excl_tax, rate)

def calculate_tax(price, rate):
    tax = price * rate
    return tax.quantize(D('0.01'))