from django.contrib import admin
from .models import Customer, SaleBill, ProductSale

# Register your models here.
admin.site.register(Customer)
admin.site.register(SaleBill)
admin.site.register(ProductSale)
