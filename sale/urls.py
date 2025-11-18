from django.urls import path
from . import views


urlpatterns = [
    path('', views.SaleBillListView.as_view(), name='salebill-list'),
    path('<int:pk>/', views.SaleBillDetailView.as_view(), name='salebill-detail'),
    path('create/', views.SaleBillCreateView.as_view(), name='salebill-create'),
]
