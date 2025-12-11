from django.db import models
from stock.models import Stock
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import reverse

# Create your models here.

class PurchaseBill(models.Model):
    bill_number = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Purchase Bill #{self.bill_number}"
    
    def save(self, *args, **kwargs):
        # Save the instance first to get a unique ID
        is_new = self.pk is None
        super(PurchaseBill, self).save(*args, **kwargs)

        if is_new:
            # Now that we have an ID, generate the unique bill number
            self.bill_number = f'PUR-{self.id:04d}'
            # Save again to update the bill_number field
            super(PurchaseBill, self).save(update_fields=['bill_number'])
    
    def get_absolute_url(self):
        return reverse('purchasebill-edit', kwargs={'pk': self.pk})


class StockPurchase(models.Model):
    purchasebill = models.ForeignKey(PurchaseBill, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at which stock was purchased
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Purchase of {self.stock.name} - {self.quantity}"
    
    def amount(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        is_new = self.pk is None # Check if this is a new instance
        super().save(*args, **kwargs) # Save the instance first

        # If it's a new instance, update the stock quantity
        if is_new:
            self.stock.purchase(self.quantity) # Call the stock's purchase method
        
        # TODO: Add logic for updating stock quantity if an existing StockPurchase is modified.
        # This would require comparing old_quantity with new_quantity.
        # For now, we're only handling initial creation.


# @receiver(post_delete, sender=StockPurchase)
# def restock_on_stock_purchase_delete(sender, instance, **kwargs):
#     """
#     When a StockPurchase is deleted, 'return' the purchased quantity from stock.
#     """
#     instance.stock.purchase_return(instance.quantity)