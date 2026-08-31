from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["thumb", "name", "category", "price", "compare_at_price", "stock", "is_active", "is_featured"]
    list_filter = ["category", "is_active", "is_featured"]
    search_fields = ["name"]
    list_editable = ["price", "stock", "is_active", "is_featured"]
    prepopulated_fields = {"slug": ("name",)}

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:45px;border-radius:6px;" />', obj.image.url)
        return "-"
    thumb.short_description = "Image"
