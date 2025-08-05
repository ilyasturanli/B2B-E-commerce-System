from django import template
from commerce_app import currency
register = template.Library()


@register.filter(name="usd_calc")
def usd_calc(data, arg):

    usd = currency.last_usd_data

    usd_product = arg * usd
    usd_product_rounded = round(usd_product,4)
    return usd_product_rounded
    print(arg)