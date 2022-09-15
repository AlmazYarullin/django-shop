import stripe
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_GET
from stripe.error import InvalidRequestError

from TestProject.apps.item.models import Item
from .checkout_session import create_checkout_session
from .models import Order, OrderItem


@require_POST
def add_item_to_order(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if order_id := request.session.get('order_id'):
        order = Order.objects.get(id=order_id)
    else:
        order = Order()
        order.save()
        request.session['order_id'] = order.id

    order_item = OrderItem.objects.filter(item=item, order=order).first()
    if order_item:
        order_item.quantity += 1
    else:
        order_item = OrderItem(item=item, order=order)
    order_item.save()
    request.session['items_in_cart'] = request.session.get('items_in_cart', 0) + 1

    return redirect('item', item_id=item_id)


@require_GET
def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    order = Order()
    order.save()
    order_item = OrderItem(order=order, item=item)
    order_item.save()
    session = create_checkout_session(request, order.id)
    return JsonResponse(session)


@require_GET
def buy_cart(request, order_id):
    session = create_checkout_session(request, order_id=order_id)
    return JsonResponse(session)


@require_GET
def success_payment(request):
    try:
        session: stripe.checkout.Session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))
    except InvalidRequestError:
        raise Http404()
    if session.payment_status == 'paid':
        order = Order.objects.get(id=request.session['order_id'])
        order.paid = True
        request.session.pop('order_id')
        request.session.pop('items_in_cart')
        return render(request, 'success.html')
    return redirect('cancel_payment')


@require_GET
def cancel_payment(request):
    return render(request, 'cancel.html')
