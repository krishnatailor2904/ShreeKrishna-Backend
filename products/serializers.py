from rest_framework import serializers
from .models import Category, Product
import cloudinary.utils


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(
        source="products.count",
        read_only=True
    )

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "product_count"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )
    category_slug = serializers.CharField(
        source="category.slug",
        read_only=True
    )

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if not obj.image:
            return None

        url, options = cloudinary.utils.cloudinary_url(
            obj.image.name,
            secure=True
        )

        return url

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "compare_at_price",
            "discount_percent",
            "image",
            "is_featured",
            "stock",
            "category",
            "category_name",
            "category_slug",
        ]