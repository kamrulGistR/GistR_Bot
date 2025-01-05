# bot_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/order/<str:tracking_code>/', views.order_status, name='order_status'),
]