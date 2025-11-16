from django import forms
from django.forms import inlineformset_factory
from .models import Product, StockVariant

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define common Tailwind CSS classes for the input fields
        input_classes = 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 p-4 text-base font-normal leading-normal'
        
        # Apply classes and placeholders to the form fields
        self.fields['name'].widget.attrs.update({
            'class': input_classes,
            'placeholder': 'e.g., CR7 9ml Perfume'
        })
        self.fields['price'].widget.attrs.update({
            'class': input_classes,
            'placeholder': 'e.g., 199.00',
            'step': '0.01' # Good practice for decimal fields
        })

    class Meta:
        model = Product
        fields = ['name', 'price']



# 💡 FIX: Explicitly set fk_name to 'product'
StockVariantInlineFormset = inlineformset_factory(
    Product, 
    StockVariant, 
    fields=['stock', 'quantity'], 
    extra=0,
    can_delete=True, # Ensure deletion is enabled for the UpdateView
    fk_name='product', # Tells the formset exactly which FK in StockVariant links to Product
    min_num=1,  # <--- THIS IS THE ONLY CHANGE YOU NEED IN PYTHON
    validate_min=True, # Optional: Ensures validation error if min not met
    widgets={
        'quantity': forms.NumberInput(attrs={
            'class': 'form-input w-full resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 text-base font-normal leading-normal text-center',
            'placeholder': 'Qty'
        }),
        # Note: 'stock' is a ForeignKey, its widget is a Select. We style it with Select2 in the template.
    }
)
