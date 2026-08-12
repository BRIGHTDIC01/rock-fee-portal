from django.urls import path
from .views import register_student, student_portal


urlpatterns = [
    path(
        "register/",
        register_student,
        name="register_student",
    ),

    path(
        "portal/",
        student_portal,
        name="student_portal",
    ),
]