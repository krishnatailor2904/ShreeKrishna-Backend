from django.http import HttpResponse
from .models import Product


def product_sitemap(request):
    products = Product.objects.filter(is_active=True)

    urls = [
        "https://shreekrishnaa.com/",
        "https://shreekrishnaa.com/shop",
        "https://shreekrishnaa.com/about",
        "https://shreekrishnaa.com/contact",
    ]

    urls += [
        f"https://shreekrishnaa.com/product/{product.slug}"
        for product in products
    ]

    xml_urls = "\n".join(
        f"""    <url>
        <loc>{url}</loc>
    </url>"""
        for url in urls
    )

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_urls}
</urlset>"""

    return HttpResponse(
        xml,
        content_type="application/xml"
    )