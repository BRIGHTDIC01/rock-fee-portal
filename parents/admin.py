from django.contrib import admin
from .models import Parent


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "phone",
        "user",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "user__username",
        "user__email",
    )

    filter_horizontal = (
        "students",
    )