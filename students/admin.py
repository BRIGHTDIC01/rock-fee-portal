from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "full_name",
        "student_class",
        "parent_name",
        "parent_phone",
        "registered_at",
        "is_active",
    )

    search_fields = (
        "student_id",
        "full_name",
        "parent_name",
        "parent_phone",
    )

    list_filter = (
        "student_class",
        "is_active",
    )