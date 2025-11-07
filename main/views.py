from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

# Create your views here.

def home(request):
    return render(request, 'main/home.html')


class Home(View):
    def get(self, request):
        return HttpResponse("This is MAIN from Class Based View")