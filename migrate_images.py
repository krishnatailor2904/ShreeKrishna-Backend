import os
from pathlib import Path

import cloudinary
import cloudinary.uploader

from django.conf import settings
from products.models import Product


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

print("====================================")
print("Cloudinary:", cloudinary.config().cloud_name)
print("====================================")

if not cloudinary.config().cloud_name:
    print("❌ CLOUDINARY_CLOUD_NAME missing")
    raise SystemExit

if not cloudinary.config().api_key:
    print("❌ CLOUDINARY_API_KEY missing")
    raise SystemExit

if not cloudinary.config().api_secret:
    print("❌ CLOUDINARY_API_SECRET missing")
    raise SystemExit


MEDIA_PRODUCTS = Path(settings.MEDIA_ROOT) / "products"

print("Image folder:", MEDIA_PRODUCTS)
print()


products = Product.objects.all().order_by("id")

success = 0
failed = 0


for product in products:

    current = str(product.image)
    base_name = Path(current).name

    matches = list(MEDIA_PRODUCTS.glob(base_name + ".*"))

    if not matches:
        print(
            f"❌ NOT FOUND | ID {product.id} | "
            f"{product.name} | {base_name}"
        )
        failed += 1
        continue

    local_file = matches[0]

    print(
        f"⬆️ Uploading | ID {product.id} | "
        f"{product.name} | {local_file.name}"
    )

    try:

        result = cloudinary.uploader.upload(
            str(local_file),
            folder="products",
            public_id=base_name,
            overwrite=True,
            resource_type="image",
        )

        product.image = result["public_id"]
        product.save(update_fields=["image"])

        print(f"✅ DONE | {result['secure_url']}")
        print()

        success += 1

    except Exception as e:

        print(
            f"❌ ERROR | ID {product.id} | "
            f"{product.name}"
        )

        print(e)
        print()

        failed += 1


print("====================================")
print("🎉 MIGRATION FINISHED")
print("SUCCESS:", success)
print("FAILED:", failed)
print("====================================")