from django.urls import path
from main.views import *

urlpatterns = [
    path('home', home, name='home'),
    path('products', product_list, name='product_list'),
    path('search/', search_view, name='search'),
    path('product/<int:product_id>/', product_detail_view, name='product_detail'),
    path('like/<int:product_id>/', like_product, name='like_product'),
]