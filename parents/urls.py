from django.urls import path

from . import views


urlpatterns = [

    path(
        "register/",
        views.parent_register,
        name="parent_register"
    ),

    path(
        "login/",
        views.parent_login,
        name="parent_login"
    ),

    path(
        "dashboard/",
        views.parent_dashboard,
        name="parent_dashboard"
    ),

    path(
        "add-student/",
        views.add_student,
        name="add_student"
    ),

    path(
        "logout/",
        views.parent_logout,
        name="parent_logout"
    ),
]