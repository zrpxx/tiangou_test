from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('users', views.getAllUser),
    path('categories', views.getAllCategory),
    path('category/create', views.createCategory),
    path('category/update', views.updateCategory),
    path('category/delete', views.deleteCategory),
    path('properties/<int:category_id>', views.getAllProperty),
    path('property/create', views.createProperty),
    path('property/update', views.updateProperty),
    path('property/delete', views.deleteProperty),
    path('products', views.getAllProduct),
    path('product/get/<int:product_id>', views.getProduct),
    path('product/create', views.createProduct),
    path('product/update', views.updateProduct),
    path('product/delete', views.deleteProduct),
    path('product_image/update', views.updateProductImage),
    path('product_property', views.setProductPropertyValue),
    path('orders', views.getAllOrder),
    path('order/get/<int:order_id>', views.getOrder),
    path('order/update', views.updateOrder)
]
