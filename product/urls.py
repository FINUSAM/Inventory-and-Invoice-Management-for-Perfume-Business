from django.urls import path
from . import views

urlpatterns = [
    path('function/', views.home, name='home'),
    path('class/', views.Home.as_view(), name='home'),

    path('', views.ProductListView.as_view(), name='product-list'),

    # path('create/', views.ProductCreateView.as_view(), name='product-create'),
    # path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-edit'),
    # path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

]
