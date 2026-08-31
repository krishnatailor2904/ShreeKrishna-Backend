from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.category_list),
    path("", views.product_list),
    path("<slug:slug>/", views.product_detail),
]
