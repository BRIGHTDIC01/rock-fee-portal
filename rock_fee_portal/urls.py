from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def home(request):

    return redirect(
        "parent_register"
    )


urlpatterns = [

    # Homepage
    path(
        "",
        home,
        name="home"
    ),

    # Staff Dashboard
    path(
        "staff-dashboard/",
        include("dashboard.urls")
    ),

    # Django Admin
    path(
        "admin/",
        admin.site.urls
    ),

    # Fees
    path(
        "fees/",
        include("fees.urls")
    ),

    # Parent Portal
    path(
        "parent/",
        include("parents.urls")
    ),
]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )