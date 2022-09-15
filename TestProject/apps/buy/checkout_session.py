import stripe
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Order


def create_checkout_session(request: HttpRequest, order_id) -> stripe.checkout.Session:
    order = get_object_or_404(Order, id=order_id)
    line_items = []
    discount_id = None

    if order.discount:
        discount_id = order.discount.discount_id

    for order_item in order.orderitem_set.all():
        line_item = {
            'quantity': order_item.quantity,
            'price_data': {
                'currency': 'usd',
                'unit_amount': order_item.item.price * 100,
                'product_data': {
                    'name': order_item.item.name,
                },
            },
        }
        if order.tax:
            line_item['tax_rates'] = [order.tax.tax_rate_id]
        line_items.append(line_item)

    session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success_payment')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('cancel_payment')),
        discounts=[{
            'coupon': discount_id
        }]
    )
    return session
