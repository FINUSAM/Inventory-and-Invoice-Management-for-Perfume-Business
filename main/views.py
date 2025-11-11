from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    return render(request, 'main/home.html')


class Home(View):
    def get(self, request):
        return HttpResponse("This is MAIN from Class Based View")