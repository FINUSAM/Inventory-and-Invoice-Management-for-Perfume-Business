from django import forms
from django.forms import inlineformset_factory
from .models import SaleBill, ProductSale
from product.models import Product


class SaleBillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_classes = 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 p-4 text-base font-normal leading-normal'
        select_classes = 'form-select appearance-none flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 pl-4 pr-10 text-base font-normal leading-normal'
        
        self.fields['customer'].widget.attrs.update({'class': select_classes})
        self.fields['discount'].widget.attrs.update({
            'class': input_classes,
            'placeholder': 'e.g., 50.00'
        })

    class Meta:
        model = SaleBill
        fields = ['customer', 'discount']


SaleBillInlineFormset = inlineformset_factory(
    SaleBill, 
    ProductSale, 
    fields=['product', 'quantity', 'price'], 
    extra=0,
    can_delete=True, # Ensure deletion is enabled for the UpdateView
    fk_name='salebill', # Tells the formset exactly which FK in ProductSale links to SaleBill
    min_num=1,  # <--- THIS IS THE ONLY CHANGE YOU NEED IN PYTHON
    validate_min=True, # Optional: Ensures validation error if min not met,
    widgets={
        'quantity': forms.NumberInput(attrs={
            'class': 'form-input w-full resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 text-base font-normal leading-normal text-center',
            'placeholder': 'Qty'
        }),
        'price': forms.NumberInput(attrs={
            'class': 'form-input w-full resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 text-base font-normal leading-normal text-center',
            'placeholder': 'Price'
        }),
        # 'product' is a ForeignKey, its widget is a Select. We style it with Select2 in the template/JS.
    }
)
