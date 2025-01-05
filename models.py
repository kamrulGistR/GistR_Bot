# bot_app/models.py

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    user_type = models.CharField(max_length=20)  # customer, restaurant, rider
    verified = models.BooleanField(default=False)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    tracking_code = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="Pending")
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deliveries', null=True, blank=True)

class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    verified = models.BooleanField(default=False)