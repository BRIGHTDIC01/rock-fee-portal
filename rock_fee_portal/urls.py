from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


# ============================================================
# HOMEPAGE
# ============================================================

def home(request):
    return redirect("parent_register")


# ============================================================
# URL PATTERNS
# ============================================================

urlpatterns = [

    # Homepage
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
# MEDIA FILES
# ============================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )