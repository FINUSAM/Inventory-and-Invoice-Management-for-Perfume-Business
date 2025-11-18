from .models import SaleBill, ProductSale
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SaleBillForm, SaleBillInlineFormset
from django.shortcuts import redirect

# Create your views here.

class SaleBillListView(LoginRequiredMixin, ListView):
    model = SaleBill


class SaleBillDetailView(LoginRequiredMixin, DetailView):
    model = SaleBill
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salebill = self.object
        product_sales = ProductSale.objects.filter(salebill=salebill)
        context['product_sales'] = product_sales
        return context


class SaleBillCreateView(LoginRequiredMixin, CreateView):
    model = SaleBill
    form_class = SaleBillForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in kwargs:
            context['formset'] = SaleBillInlineFormset(queryset=ProductSale.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        formset = SaleBillInlineFormset(request.POST)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        salebill = form.save()

        # Now save each ProductSale instance from the formset
        for product_sale in formset.save(commit=False):
            product_sale.salebill = salebill  # Link ProductSale to the SaleBill
            product_sale.save()

        # Redirect to the sale bill detail view or another page after successful submission
        return redirect('salebill-list')


    def form_invalid(self, form, formset):
        # If the form or formset is invalid, re-render the form with error messages
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
