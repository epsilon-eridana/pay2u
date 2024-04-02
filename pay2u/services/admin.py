from django.contrib import admin

from .models import (
    Service, Category, Rate, Option, ServiceRate,
    ServiceOptions, Tag, Image, ServiceImage
)


class ServiceRateInline(admin.TabularInline):
    model = ServiceRate
    extra = 1


class ServiceOptionsInline(admin.TabularInline):
    model = ServiceOptions
    extra = 1


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 2


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'category', 'short_description'
    )
    inlines = [
        ServiceRateInline, ServiceOptionsInline, ServiceImageInline
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'slug'
    )
    prepopulated_fields = {'slug': ('name',)}


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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'slug', 'color'
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Image)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image'
    )
