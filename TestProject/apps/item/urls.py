from django.urls import path

from TestProject.apps.item import views

urlpatterns = [
    path('<int:item_id>', views.show_item, name='item'),
]
