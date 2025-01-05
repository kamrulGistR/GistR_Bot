# bot_app/admin.py

from django.contrib import admin
from .models import User, Order, Restaurant

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'user_type', 'verified')
    actions = ['verify_user']

    def verify_user(self, request, queryset):
        queryset.update(verified=True)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'status', 'customer', 'rider')

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'verified')
    actions = ['verify_restaurant']

    def verify_restaurant(self, request, queryset):
        queryset.update(verified=True)