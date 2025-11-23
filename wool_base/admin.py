from django.contrib import admin
from .models import Shop, Product, Offer


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "base_url")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("brand", "name")
    search_fields = ("brand", "name")
    list_filter = ("brand",)
    ordering = ("brand", "name")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "shop",
        "price",
        "availability",
        "needle_size",
        "last_updated_at",
    )
    list_filter = (
        "shop",
        "availability",
    )
    search_fields = (
        "product__brand",
        "product__name",
        "composition",
    )
    ordering = ("product__brand", "product__name", "shop__name")
    list_editable = ("price", "availability")
    readonly_fields = ("last_updated_at",)
