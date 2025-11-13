from django.db import models
from product.models import Product
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SaleBill(models.Model):
    bill_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def amount(self):
        total = sum(item.amount() for item in self.productsale_set.all())
        return total
    
    @property
    def final_amount(self):
        return self.amount - self.discount

    def __str__(self):
        return f"Bill for {self.customer.name if self.customer else 'Walk-in Customer'} - {self.final_amount}"

    def save(self, *args, **kwargs):
        if not self.customer:
            walk_in_customer, created = Customer.objects.get_or_create(name="Walk-in Customer")
            self.customer = walk_in_customer

        # Save the instance first to get a unique ID
        is_new = self.pk is None
        super(SaleBill, self).save(*args, **kwargs)

        if is_new:
            # Now that we have an ID, generate the unique bill number
            self.bill_number = f'EMZA-{self.id:04d}'
            # Save again to update the bill_number field
            super(SaleBill, self).save(update_fields=['bill_number'])



class ProductSale(models.Model):
    salebill = models.ForeignKey(SaleBill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sale of {self.product.name} - {self.quantity}"
    
    def amount(self):
        return self.quantity * self.price
    
    def clean(self):
        super().clean()
        if self.product and self.quantity:
            if self.product.available_quantity < self.quantity:
                raise ValidationError(f"Not enough stock for {self.product.name}. Only {self.product.available_quantity} available.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Always run validation before saving
        if self.price is None and self.product:
            self.price = self.product.price
        self.product.sale(self.quantity)
        super().save(*args, **kwargs)


@receiver(post_delete, sender=ProductSale)
def restock_on_product_sale_delete(sender, instance, **kwargs):
    """
    When a ProductSale is deleted, restock the product by the quantity
    that was in the sale.
    """
    instance.product.sale_return(instance.quantity)
