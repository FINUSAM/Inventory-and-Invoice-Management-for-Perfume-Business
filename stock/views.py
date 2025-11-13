from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


from .models import Stock
from django.views.generic import ListView

# Create your views here.

def home(request):
    return HttpResponse("This is MAIN from Function Based View")

class StockListView(ListView):
    model = Stock

class Home(View):
    def get(self, request):
        return HttpResponse("This is MAIN from Class Based View")