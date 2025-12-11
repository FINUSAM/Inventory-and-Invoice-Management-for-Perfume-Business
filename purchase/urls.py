from django.urls import path
from . import views

urlpatterns = [
    path('', views.PurchaseBillListView.as_view(), name='purchasebill-list'),
    path('create/', views.PurchaseBillCreateView.as_view(), name='purchasebill-create'),
    path('<int:pk>/edit/', views.PurchaseBillUpdateView.as_view(), name='purchasebill-edit'),
]
