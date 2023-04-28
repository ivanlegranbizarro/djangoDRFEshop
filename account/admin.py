from django.contrib import admin

from .models import MyUser, Profile

# Register your models here.


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_active", "date_joined")
    search_fields = ("email", "first_name", "last_name", "username")
    ordering = ("email",)
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Profile)
