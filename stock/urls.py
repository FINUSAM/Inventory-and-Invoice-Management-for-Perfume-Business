from django.urls import path
from . import views

urlpatterns = [
    path('function/', views.home, name='home'),
    path('class/', views.Home.as_view(), name='home'),

    path('', views.StockListView.as_view(), name='stock-list'),



    # path('business/<int:business_id>/stock-search/', views.stock_search_ajax_view, name='stock_search_ajax'),

    

]
