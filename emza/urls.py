from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),
    path('stocks/', include('stock.urls')),
    path('products/', include('product.urls')),
    path('sales/', include('sale.urls')),
    path('customers/', include('customer.urls')),
    path('', include('main.urls')),
]

