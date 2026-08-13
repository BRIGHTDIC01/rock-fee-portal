from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect


# ============================================================
# HOME
# ============================================================

def home(request):
    return redirect("parent_login")


# ============================================================
# URL PATTERNS
# ============================================================

urlpatterns = [

    # Main Website
    path(
        "",
        home,
        name="home"
    ),

    # Django Admin
    path(
        "admin/",
        admin.site.urls
    ),

    # Fees App
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


# ============================================================
# MEDIA / STATIC FILES
# ============================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )