from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductVideo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # 3 khaali image slots by default; "Add another" se aur bhi add kar sakte ho
    fields = ["image", "order", "preview"]
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', obj.image.url)
        return "-"
    preview.short_description = "Preview"


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 1  # 1 khaali video slot by default; "Add another" se aur bhi add kar sakte ho
    fields = ["video", "order"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["thumb", "name", "category", "price", "compare_at_price", "stock", "is_active", "is_featured"]
    list_filter = ["category", "is_active", "is_featured"]
    search_fields = ["name"]
    list_editable = ["price", "stock", "is_active", "is_featured"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductVideoInline]

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:45px;border-radius:6px;" />', obj.image.url)
        return "-"
    thumb.short_description = "Image"