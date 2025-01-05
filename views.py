# bot_app/views.py

from django.http import JsonResponse
from .models import Order

def order_status(request, tracking_code):
    try:
        order = Order.objects.get(tracking_code=tracking_code)
        return JsonResponse({'status': order.status})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)