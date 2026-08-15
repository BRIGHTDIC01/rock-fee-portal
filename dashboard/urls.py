from django.urls import path
from . import views


app_name = "dashboard"


urlpatterns = [

    # ========================================================
    # MAIN DASHBOARD
    # ========================================================

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),


    # ========================================================
    # STUDENTS
    # ========================================================

    path(
        "students/",
        views.student_list,
        name="student_list"
    ),

    path(
        "students/<int:student_id>/",
        views.student_detail,
        name="student_detail"
    ),

    path(
        "students/<int:student_id>/toggle-status/",
        views.toggle_student_status,
        name="toggle_student_status"
    ),


    # ========================================================
    # PAYMENTS
    # ========================================================

    path(
        "payments/",
        views.payment_list,
        name="payment_list"
    ),

    path(
        "payments/<int:payment_id>/",
        views.payment_detail,
        name="payment_detail"
    ),

    path(
        "payments/download-excel/",
        views.download_payments_excel,
        name="download_payments_excel"
    ),

]