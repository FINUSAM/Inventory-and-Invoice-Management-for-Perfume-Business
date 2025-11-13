from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .models import SaleBill, ProductSale
from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    return HttpResponse("This is MAIN from Function Based View")

class SaleBillListView(ListView):
    model = SaleBill


class SaleBillDetailView(LoginRequiredMixin, DetailView):
    model = SaleBill
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salebill = self.object
        product_sales = ProductSale.objects.filter(salebill=salebill)
        context['product_sales'] = product_sales
        return context



class Home(View):
    def get(self, request):
        return HttpResponse("This is MAIN from Class Based View")