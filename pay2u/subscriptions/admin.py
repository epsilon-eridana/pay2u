from django.contrib import admin

from .models import (
    Service, Category, Rate, Option, ServiceRate, ServiceOptions
)


class ServiceRateInline(admin.TabularInline):
    model = ServiceRate
    extra = 1


class ServiceOptionsInline(admin.TabularInline):
    model = ServiceOptions
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'category', 'short_description'
    )
    inlines = [ServiceRateInline, ServiceOptionsInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'slug'
    )


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name'
    )


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'price', 'duration', 'cashback'
    )
