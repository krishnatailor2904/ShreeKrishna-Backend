from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "Create the default Shree Krishnaa admin/superuser account."

    def handle(self, *args, **options):
        email = "admin@shreekrishnaa.com"
        password = "Krishna@123"

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Admin user {email} already exists — skipping."))
            return

        User.objects.create_superuser(
            email=email,
            full_name="ShreeKrishnaa",
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(
            f"Admin created!\n  Login email: {email}\n  Password: {password}\n"
            f"  (Log in at /admin/ — change this password after first login)"
        ))
