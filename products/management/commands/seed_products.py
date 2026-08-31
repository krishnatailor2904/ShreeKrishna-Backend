import os
from django.core.files import File
from django.core.management.base import BaseCommand

from products.models import Category, Product

SEED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "seed_images")

# (filename, category name, product name, price, compare_at_price, featured)
DATA = [
    ("Acrlic.jpg", "Acrylic Name Plates", "Police Desk Nameplate — Classic Acrylic", 349, 499, True),
    ("Acrlic_1.jpg", "Acrylic Name Plates", "Acrylic Desk Nameplate — Design 1", 349, 499, False),
    ("Acrlic_2.jpg", "Acrylic Name Plates", "Acrylic Desk Nameplate — Design 2", 349, 499, False),
    ("Acrlic_3.jpg", "Acrylic Name Plates", "Acrylic Desk Nameplate — Design 3", 379, 549, False),
    ("Acrlic_4.jpg", "Acrylic Name Plates", "Acrylic Desk Nameplate — Design 4", 379, 549, False),
    ("Acrlic_5.jpg", "Acrylic Name Plates", "Acrylic Desk Nameplate — Design 5", 399, 599, True),
    ("Acrlic_6.jpg", "Acrylic Name Plates", "Acrylic Desk Nameplate — Design 6", 399, 599, False),
    ("Acrlic_7.jpg", "Acrylic Name Plates", "Acrylic Desk Nameplate — Design 7", 419, 599, False),
    ("Acrlic_8.jpg", "Acrylic Name Plates", "Acrylic Desk Nameplate — Design 8", 419, 599, False),
    ("Acrlic_9.jpg", "Acrylic Name Plates", "Acrylic Desk Nameplate — Design 9", 449, 649, False),
    ("Acrlic_10.jpg", "Acrylic Name Plates", "Acrylic Desk Nameplate — Design 10", 449, 649, False),

    ("Metal.jpg", "Metal Name Plates", "Premium Metal Desk Nameplate", 599, 799, True),
    ("Metall.jpg", "Metal Name Plates", "Metal Desk Nameplate — Brushed Finish", 599, 799, False),
    ("Metal_English_Silver.jpg", "Metal Name Plates", "Metal Nameplate — English (Silver)", 649, 899, True),
    ("Metal_Gujarati_Silver.jpg", "Metal Name Plates", "Metal Nameplate — Gujarati (Silver)", 649, 899, False),
    ("Metal_Gold_English.jpg", "Metal Name Plates", "Metal Nameplate — English (Gold)", 749, 999, True),
    ("Metal_Gold_Gujarati.jpg", "Metal Name Plates", "Metal Nameplate — Gujarati (Gold)", 749, 999, False),

    ("Hotel_Staff.jpg", "Hotel Staff Badges", "Hotel Staff Name Badge", 199, 299, True),
    ("Hotel_stafff.jpg", "Hotel Staff Badges", "Hotel Staff Name Badge — Premium", 229, 329, False),

    ("Doctor.jpg", "Doctor Name Plates", "Doctor Clinic Nameplate", 449, 649, True),
]


class Command(BaseCommand):
    help = "Seed the database with categories and products from the uploaded sample images."

    def handle(self, *args, **options):
        created_products = 0
        created_categories = 0

        for filename, cat_name, prod_name, price, compare_price, featured in DATA:
            category, was_created = Category.objects.get_or_create(name=cat_name)
            if was_created:
                created_categories += 1

            if Product.objects.filter(name=prod_name).exists():
                continue

            img_path = os.path.join(SEED_DIR, filename)
            if not os.path.exists(img_path):
                self.stdout.write(self.style.WARNING(f"Missing image: {img_path}"))
                continue

            product = Product(
                category=category,
                name=prod_name,
                description=(
                    f"High-quality {prod_name.lower()} — durable build, sharp engraving, "
                    f"and fast custom-name production. Perfect for daily duty wear or desk display."
                ),
                price=price,
                compare_at_price=compare_price,
                is_featured=featured,
                stock=100,
            )
            with open(img_path, "rb") as f:
                product.image.save(filename, File(f), save=True)
            created_products += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete: {created_categories} categories, {created_products} products created."
        ))
