from django import template

register = template.Library()


@register.filter(name='three_digit_currency')
def three_digit_currency(value: int):
    return '{:,}'.format(value) + ' تومان'
