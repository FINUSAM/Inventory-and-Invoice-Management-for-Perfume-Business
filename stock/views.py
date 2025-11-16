from .models import Stock
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

# Create your views here.

class StockListView(ListView):
    model = Stock


class StockCreateView(CreateView):
    model = Stock
    fields = ['name', 'stock_type','opening_quantity']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Common classes for text/number inputs
        input_classes = 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 p-4 text-base font-normal leading-normal'
        
        # Classes for the select dropdown
        select_classes = 'form-select appearance-none flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 pl-4 pr-10 text-base font-normal leading-normal'

        form.fields['name'].widget.attrs.update({'class': input_classes, 'placeholder': 'e.g., CR7'})
        form.fields['opening_quantity'].widget.attrs.update({'class': input_classes, 'placeholder': 'e.g., 100'})
        form.fields['stock_type'].widget.attrs.update({'class': select_classes})
        return form