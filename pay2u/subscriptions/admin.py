from django.contrib import admin

from .models import Subscription, Payment


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'rate', 'date_start',
        'date_end', 'extension'
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'rate', 'price',
        'cashback', 'date', 'type', 'user'
    )
