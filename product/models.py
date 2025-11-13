from django.db import models, transaction
from stock.models import Stock

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def available_quantity(self):
        # Fetch all StockVariants related to this Product
        stock_variants = StockVariant.objects.filter(product=self)

        # Initialize a list to store how many products can be made by each stock variant
        product_counts = []

        # Iterate over each StockVariant to calculate the number of products that can be created
        for stock_variant in stock_variants:
            stock = stock_variant.stock
            available_quantity = stock.balance_quantity
            products_from_variant = available_quantity // stock_variant.quantity
            product_counts.append(products_from_variant)

        # The final number of products we can create is limited by the stock variant that can make the least products
        return min(product_counts) if product_counts else 0


    def sale(self, product_quantity):
        with transaction.atomic():
            # Re-check availability inside the transaction to prevent race conditions
            if self.available_quantity < product_quantity:
                raise ValueError(f"Not enough stock available for {self.name}. Only {self.available_quantity} left.")
            
            stock_variants = StockVariant.objects.filter(product=self)
            for stock_variant in stock_variants:
                quantity_to_deduct = stock_variant.quantity * product_quantity
                stock_variant.stock.sale(quantity_to_deduct)

    def purchase(self, product_quantity):
        with transaction.atomic():
            stock_variants = StockVariant.objects.filter(product=self)
            for stock_variant in stock_variants:
                quantity_to_add = stock_variant.quantity * product_quantity
                stock_variant.stock.purchase(quantity_to_add)

    def sale_return(self, product_quantity):
        with transaction.atomic():
            stock_variants = StockVariant.objects.filter(product=self)
            for stock_variant in stock_variants:
                quantity_to_deduct = stock_variant.quantity * product_quantity
                stock_variant.stock.sale_return(quantity_to_deduct)

    def __str__(self):
        return self.name


class StockVariant(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['stock', 'product'], 
                name='unique_stock_per_product',
                violation_error_message="stock with the same name already exists for this product."
            )
        ]

    def __str__(self):
        return f"{self.product.name} ({self.stock.name})"
