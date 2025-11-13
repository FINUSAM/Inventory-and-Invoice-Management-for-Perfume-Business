from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .models import Product
from django.views.generic import ListView

# Create your views here.

def home(request):
    return render(request, 'product/product_list.html')

class ProductListView(ListView):
    model = Product


class Home(View):
    def get(self, request):
        return HttpResponse("This is MAIN from Class Based View")