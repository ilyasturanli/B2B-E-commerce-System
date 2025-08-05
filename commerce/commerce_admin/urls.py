from django.urls import path
from . import views
urlpatterns = [
    path('', views.panel_home, name="panel-home"),
    path('orders/', views.panel_orders, name="panel-orders"),
    path('order-detail/<int:order_id>/', views.panel_order_detail, name='panel-order-detail'),
    path('panel-login/', views.panel_login, name="panel-login"),
    path('panel-logout/', views.panel_logout, name="panel-logout")
]
