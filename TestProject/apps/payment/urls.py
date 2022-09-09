from django.urls import path

from TestProject.apps.payment import views

urlpatterns = [
    path('<int:item_id>', views.create_checkout_session, name='create_checkout_session'),
    path('success', views.success_payment, name='success_payment'),
    path('cancel', views.cancel_payment, name='cancel_payment'),
]
