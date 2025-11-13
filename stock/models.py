from django.db import models
from django.urls import reverse

# Create your models here.


class MetricChoices(models.TextChoices):
    PIECE = "pcs", "Pieces"
    Milliliter = "ml", "Milliliters"


class StockType(models.Model):
    name = models.CharField(max_length=255)
    metric = models.CharField(max_length=10, choices=MetricChoices.choices, default=MetricChoices.PIECE, help_text="Unit of measurement (e.g. ml, pcs)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.metric})"



class Stock(models.Model):
    name = models.CharField(max_length=255, unique=True)
    stock_type = models.ForeignKey(StockType, on_delete=models.CASCADE)
    purchase_quantity = models.IntegerField(default=0)
    sale_quantity = models.IntegerField(default=0)
    opening_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def balance_quantity(self):
        return self.opening_quantity + self.purchase_quantity - self.sale_quantity

    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse('stock-detail', kwargs={'business_id': self.business.pk, 'pk': self.pk})
    
    def metric(self):
        return self.stock_type.metric
    
    def sale(self, quantity):
        if quantity > self.balance_quantity:
            pass #raise ValueError("Not enough stock to sell.")
        
        self.sale_quantity += quantity
        self.save()
        return self.sale_quantity
    
    def purchase(self, quantity):
        self.purchase_quantity += quantity
        self.save()
        return self.purchase_quantity
    
    def sale_return(self, quantity):
        self.sale_quantity -= quantity
        self.save()
        return self.sale_quantity
