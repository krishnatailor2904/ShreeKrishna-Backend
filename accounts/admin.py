from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, OTP


class UserAdmin(BaseUserAdmin):
    ordering = ["-date_joined"]
    list_display = ["email", "full_name", "phone", "city", "is_staff", "is_active", "date_joined"]
    search_fields = ["email", "full_name", "phone"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "phone", "address_line", "city", "state", "pincode")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "phone", "password1", "password2"),
        }),
    )
    filter_horizontal = ("groups", "user_permissions")


admin.site.register(User, UserAdmin)
admin.site.register(OTP)

admin.site.site_header = "Shree Krishnaa Admin"
admin.site.site_title = "Shree Krishnaa Admin"
admin.site.index_title = "Store Management"
