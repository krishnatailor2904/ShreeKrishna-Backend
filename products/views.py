from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


@api_view(["GET"])
def category_list(request):
    categories = Category.objects.all()
    return Response(CategorySerializer(categories, many=True).data)


@api_view(["GET"])
def product_list(request):
    qs = Product.objects.filter(is_active=True)

    category = request.GET.get("category")
    if category:
        qs = qs.filter(category__slug=category)

    search = request.GET.get("search")
    if search:
        qs = qs.filter(name__icontains=search)

    featured = request.GET.get("featured")
    if featured == "true":
        qs = qs.filter(is_featured=True)

    ordering = request.GET.get("ordering")
    if ordering in ["price", "-price", "-created_at", "created_at"]:
        qs = qs.order_by(ordering)

    return Response(ProductSerializer(qs, many=True, context={"request": request}).data)


@api_view(["GET"])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug, is_active=True)
    except Product.DoesNotExist:
        return Response({"detail": "Product not found."}, status=404)
    return Response(ProductSerializer(product, context={"request": request}).data)
