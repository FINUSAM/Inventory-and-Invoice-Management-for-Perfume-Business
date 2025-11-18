from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer

# Create your views here.

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = ['name', 'phone_number', 'address']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Common classes for text/number inputs
        input_classes = 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 p-4 text-base font-normal leading-normal'
        
        form.fields['name'].widget.attrs.update({'class': input_classes, 'placeholder': 'e.g., Imran'})
        form.fields['phone_number'].widget.attrs.update({'class': input_classes, 'placeholder': 'e.g., 9876543210'})
        form.fields['address'].widget.attrs.update({'class': input_classes, 'placeholder': 'e.g., 123 Main St, Anytown'})
        return form
