from django.urls import path
from . import views


urlpatterns = [
    path('function/', views.home, name='home'),
    path('class/', views.Home.as_view(), name='home'),

    path('', views.SaleBillListView.as_view(), name='salebill-list'),
]
