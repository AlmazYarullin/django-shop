from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/', include('TestProject.apps.payment.urls')),
    path('item/', include('TestProject.apps.item.urls'))
]
