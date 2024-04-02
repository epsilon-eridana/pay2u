from django.contrib import admin

from .models import Subscription, Payment


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'rate', 'date_start', 'date_end'
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'subscription', 'price', 'cashback', 'date'
    )
