from django.conf import settings
from django.shortcuts import render, get_object_or_404

from .models import Item


def show_item(request, item_id):
    if request.method == 'GET':
        item = get_object_or_404(Item, id=item_id)
        print(item)
        return render(request, 'item.html', context={'item': item, 'stripe_client_key': settings.STRIPE_CLIENT_KEY})
