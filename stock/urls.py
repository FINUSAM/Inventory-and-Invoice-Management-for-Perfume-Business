from django.urls import path
from . import views

urlpatterns = [
    path('', views.StockListView.as_view(), name='stock-list'),
    path('create/', views.StockCreateView.as_view(), name='stock-create'),
    path('<int:pk>/edit/', views.StockUpdateView.as_view(), name='stock-edit'),
    path('search/', views.stock_search_ajax_view, name='stock_search_ajax'),
]
