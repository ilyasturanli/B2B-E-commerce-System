from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('detail/<int:product_id>/', views.detail, name="detail"),
    path('order/', views.order, name="order"),
    path('user-login/', views.user_login, name="user-login"),
    path('user-logout/', views.user_logout, name='user-logout'),
    path('order-success/', views.order_success, name="order-success"),
    path('profile/', views.profile, name="profile"),
    path('order-detail/<int:order_id>/', views.order_detail, name="order-detail")
    
    
    
]
