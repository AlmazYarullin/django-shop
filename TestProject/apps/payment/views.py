import stripe
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from TestProject.apps.item.models import Item


def create_checkout_session(request, item_id):
    if request.method == 'GET':
        item = get_object_or_404(Item, id=item_id)
        session: stripe.checkout.Session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name
                    },
                    'unit_amount': item.price * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success_payment')),
            cancel_url=request.build_absolute_uri(reverse('cancel_payment')),

        )
        return JsonResponse(session)


def success_payment(request):
    return render(request, 'success.html')


def cancel_payment(request):
    return render(request, 'cancel.html')

