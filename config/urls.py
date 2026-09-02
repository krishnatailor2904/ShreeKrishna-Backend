from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from products.sitemaps import ProductSitemap


sitemaps = {
    "products": ProductSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/", include("accounts.urls")),
    path("api/products/", include("products.urls")),
    path("api/orders/", include("orders.urls")),

    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )