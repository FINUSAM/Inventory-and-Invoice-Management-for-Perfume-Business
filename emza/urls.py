from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),
    path('stock/', include('stock.urls')),
    path('product/', include('product.urls')),
    path('sale/', include('sale.urls')),
    path('', include('main.urls')),
]

