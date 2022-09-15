from django.urls import path

from . import views

urlpatterns = [
    path('<int:item_id>', views.buy_item, name='buy_item'),
    path('success', views.success_payment, name='success_payment'),
    path('cancel', views.cancel_payment, name='cancel_payment'),
    path('order/<int:order_id>', views.buy_cart, name='buy_cart'),
    path('<int:item_id>/add_to_order', views.add_item_to_order, name='add_item_to_order')

]
