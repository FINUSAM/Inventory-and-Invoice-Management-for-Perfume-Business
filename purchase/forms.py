from django import forms
from django.forms.models import inlineformset_factory
from .models import PurchaseBill, StockPurchase
from stock.models import Stock

class PurchaseBillForm(forms.ModelForm):
    class Meta:
        model = PurchaseBill
        fields = [] # No direct fields, as bill_number is auto-generated

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can add custom styling or attributes to the form if needed
        # For example, if you wanted a specific input class for a field:
        # self.fields['some_field'].widget.attrs.update({'class': 'my-custom-class'})


class StockPurchaseForm(forms.ModelForm):
    class Meta:
        model = StockPurchase
        fields = ['stock', 'quantity', 'price']
        widgets = {
            'stock': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply common classes for styling
        input_classes = 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 p-4 text-base font-normal leading-normal'
        select_classes = 'form-select appearance-none flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 pl-4 pr-10 text-base font-normal leading-normal'

        self.fields['stock'].widget.attrs.update({'class': select_classes, 'placeholder': 'Select stock item'})
        self.fields['quantity'].widget.attrs.update({'class': input_classes, 'placeholder': 'e.g., 100'})
        self.fields['price'].widget.attrs.update({'class': input_classes, 'placeholder': 'e.g., 50.00'})

# Create an inline formset for StockPurchase related to PurchaseBill
StockPurchaseInlineFormset = inlineformset_factory(
    PurchaseBill,
    StockPurchase,
    form=StockPurchaseForm,
    extra=1,  # Number of empty forms to display initially
    can_delete=True,
)
