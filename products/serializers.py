from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVideo


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(
        source="products.count",
        read_only=True
    )

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "product_count"]


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if not obj.image:
            return None
        return obj.image.url

    class Meta:
        model = ProductImage
        fields = ["id", "image", "order"]


class ProductVideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()

    def get_video(self, obj):
        if not obj.video:
            return None
        return obj.video.url

    class Meta:
        model = ProductVideo
        fields = ["id", "video", "order"]


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
    images = ProductImageSerializer(many=True, read_only=True)
    videos = ProductVideoSerializer(many=True, read_only=True)

    def get_image(self, obj):
        if not obj.image:
            return None

        return obj.image.url

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
            "images",
            "videos",
            "is_featured",
            "stock",
            "category",
            "category_name",
            "category_slug",
        ]