from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


# ============================================================
# HOMEPAGE
# ============================================================

def home(request):

    return redirect(
        "parent_register"
    )


# ============================================================
# URL PATTERNS
# ============================================================

urlpatterns = [

    # --------------------------------------------------------
    # Homepage
    # --------------------------------------------------------

    path(
        "",
        home,
        name="home"
    ),


    # --------------------------------------------------------
    # Staff Dashboard
    # --------------------------------------------------------

    path(
        "staff-dashboard/",
        include("dashboard.urls")
    ),


    # --------------------------------------------------------
    # Django Admin
    # --------------------------------------------------------

    path(
        "admin/",
        admin.site.urls
    ),


    # --------------------------------------------------------
    # Fees
    # --------------------------------------------------------

    path(
        "fees/",
        include("fees.urls")
    ),


    # --------------------------------------------------------
    # Parent Portal
    # --------------------------------------------------------

    path(
        "parent/",
        include("parents.urls")
    ),
]


# ============================================================
# MEDIA FILES
#
# Payment proofs are uploaded into MEDIA_ROOT.
#
# This is deliberately enabled in production too so Render
# can serve the uploaded payment-proof files.
# ============================================================

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)