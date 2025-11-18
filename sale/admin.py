from django.contrib import admin
from .models import SaleBill, ProductSale

# Register your models here.

admin.site.register(SaleBill)
admin.site.register(ProductSale)
