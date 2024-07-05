from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('home/', views.home, name ="home"),
    path('register/', views.register, name ="home"),
    path('login/', views.login, name ="login"),
    path('cart/', views.cart, name ="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="checkout"),
    
]