from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('user/info/<int:user_id>', views.getUserInfo),
    path('categories', views.getAllCategory),
    path('category/create', views.createCategory),
    path('category/update', views.updateCategory),
    path('category/delete', views.deleteCategory),
    path('properties/<int:category_id>', views.getAllProperty),
    path('property/create', views.createProperty),
    path('property/update', views.updateProperty),
    path('property/delete', views.deleteProperty),
    path('products', views.getAllProduct),
    path('product/<int:product_id>', views.getProduct),
    path('product/create', views.createProduct),
    path('product/update', views.updateProduct),
    path('product/delete', views.deleteProduct),
    path('product_image/update', views.updateProductImage),
    path('product_property/<int:product_id>', views.getPropertiesOfProduct),
    path('product_property/update', views.setProductPropertyValue),
    path('orders', views.getAllOrder),
    path('order/<int:order_id>', views.getOrder),
    path('order/get/<int:user_id>', views.getUserOrder),
    path('order/create', views.createOrder),
    path('order/pay', views.payOrder),
    path('order/deliver', views.deliverOrder),
    path('order/confirm', views.confirmOrder),
    path('random', views.randomProduct),
    path('cart/create', views.createCartProduct),
    path('cart/delete', views.deleteCartProduct),
    path('cart/products', views.getAllCartProduct)
]
