from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('search/', views.product_search_ajax_view, name='product_search_ajax'),


    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-edit'),
    # path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

]
