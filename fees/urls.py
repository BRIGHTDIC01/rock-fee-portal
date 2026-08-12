from django.urls import path

from . import views


urlpatterns = [
    path(
        "payment/<int:student_id>/",
        views.make_payment,
        name="make_payment",
    ),

    path(
        "receipt/<int:payment_id>/",
        views.receipt,
        name="receipt",
    ),

    path(
        "receipt/<int:payment_id>/download/",
        views.download_receipt,
        name="download_receipt",
    ),
]