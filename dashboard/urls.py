from django.urls import path

from . import views


app_name = "dashboard"


urlpatterns = [

    # ========================================================
    # DASHBOARD
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
        name="students"
    ),

    path(
        "students/<int:student_id>/toggle-status/",
        views.toggle_student_status,
        name="toggle_student_status"
    ),

    path(
        "students/download-excel/",
        views.download_students_excel,
        name="download_students_excel"
    ),


    # ========================================================
    # PARENTS
    # ========================================================

    path(
        "parents/",
        views.parent_list,
        name="parents"
    ),

    path(
        "parents/download-excel/",
        views.download_parents_excel,
        name="download_parents_excel"
    ),


    # ========================================================
    # FEE STRUCTURES
    # ========================================================

    path(
        "fee-structures/",
        views.fee_structure_list,
        name="fee_structures"
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


    # ========================================================
    # DOWNLOAD PAYMENTS EXCEL
    # ========================================================

    path(
        "payments/download-excel/",
        views.download_payments_excel,
        name="download_payments_excel"
    ),

]