from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import PurchaseBill, StockPurchase
from .forms import PurchaseBillForm, StockPurchaseInlineFormset


# Create your views here.

class PurchaseBillListView(LoginRequiredMixin, ListView):
    model = PurchaseBill
    template_name = 'purchase/purchasebill_list.html'
    context_object_name = 'purchase_bills'


class PurchaseBillDetailView(LoginRequiredMixin, DetailView):
    model = PurchaseBill
    template_name = 'purchase/purchasebill_detail.html'
    context_object_name = 'purchase_bill'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase_bill = self.object
        stock_purchases = StockPurchase.objects.filter(purchasebill=purchase_bill)
        context['stock_purchases'] = stock_purchases
        return context


class PurchaseBillCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseBill
    form_class = PurchaseBillForm
    template_name = 'purchase/purchasebill_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in kwargs:
            context['formset'] = StockPurchaseInlineFormset(queryset=StockPurchase.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = StockPurchaseInlineFormset(request.POST)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        purchase_bill = form.save()

        for stock_purchase in formset.save(commit=False):
            stock_purchase.purchasebill = purchase_bill
            stock_purchase.save()

        return redirect('purchasebill-list')

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class PurchaseBillUpdateView(LoginRequiredMixin, UpdateView):
    model = PurchaseBill
    form_class = PurchaseBillForm
    template_name = 'purchase/purchasebill_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = StockPurchaseInlineFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = StockPurchaseInlineFormset(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = StockPurchaseInlineFormset(request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect('purchasebill-list')

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))