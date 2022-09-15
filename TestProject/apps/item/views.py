from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET

from TestProject.apps.buy.models import Order
from .models import Item


@require_GET
def show_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    items_in_order_amount = 0
    if order_id := request.session.get('order_id'):
        items_in_order_amount = Order.objects.get(id=order_id).orderitem_set.aggregate(Sum('quantity'))['quantity__sum']
    return render(request, 'item.html', context={
        'item': item,
        'stripe_client_key': settings.STRIPE_CLIENT_KEY,
        'items_in_order_amount': items_in_order_amount
    })
