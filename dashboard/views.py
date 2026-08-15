from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from fees.models import AcademicSession, FeeStructure, Payment
from parents.models import Parent
from students.models import Student

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


# ============================================================
# STAFF DASHBOARD
# ============================================================

@staff_member_required
def dashboard(request):

    total_students = Student.objects.filter(
        is_active=True
    ).count()

    total_parents = Parent.objects.filter(
        is_active=True
    ).count()

    total_fee_structures = FeeStructure.objects.count()

    active_session = AcademicSession.objects.filter(
        is_active=True
    ).first()

    verified_payments = Payment.objects.filter(
        status="VERIFIED"
    )

    pending_payments = Payment.objects.filter(
        status="PENDING"
    )

    rejected_payments = Payment.objects.filter(
        status="REJECTED"
    )

    total_collected = (
        verified_payments.aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0")
    )

    pending_amount = (
        pending_payments.aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0")
    )

    rejected_amount = (
        rejected_payments.aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0")
    )

    expected_fees = Decimal("0")

    if active_session:

        active_students = Student.objects.filter(
            is_active=True
        )

        for student in active_students:

            fee_query = FeeStructure.objects.filter(
                session=active_session,
                student_class=student.student_class,
                student_type=student.student_type,
            )

            if student.student_class.startswith("SSS"):

                fee_query = fee_query.filter(
                    department=student.department
                )

            else:

                fee_query = fee_query.filter(
                    department__isnull=True
                )

            fee = fee_query.first()

            if fee:
                expected_fees += fee.total_fee

    outstanding = expected_fees - total_collected

    if outstanding < 0:
        outstanding = Decimal("0")

    recent_payments = (
        Payment.objects
        .select_related(
            "student",
            "fee_structure",
        )
        .order_by(
            "-transaction_date"
        )[:8]
    )

    context = {

        "total_students": total_students,

        "total_parents": total_parents,

        "total_fee_structures": total_fee_structures,

        "active_session": active_session,

        "total_collected": total_collected,

        "pending_amount": pending_amount,

        "rejected_amount": rejected_amount,

        "pending_count": pending_payments.count(),

        "rejected_count": rejected_payments.count(),

        "expected_fees": expected_fees,

        "outstanding": outstanding,

        "recent_payments": recent_payments,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


# ============================================================
# STUDENTS
# ============================================================

@staff_member_required
def student_list(request):

    students = Student.objects.all().order_by(
        "-registered_at"
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    selected_class = request.GET.get(
        "class",
        ""
    )

    selected_status = request.GET.get(
        "status",
        ""
    )

    # ========================================================
    # SEARCH
    # ========================================================

    if search:

        students = students.filter(
            Q(full_name__icontains=search)
            |
            Q(student_id__icontains=search)
            |
            Q(parent_name__icontains=search)
            |
            Q(parent_phone__icontains=search)
        )

    # ========================================================
    # CLASS FILTER
    # ========================================================

    if selected_class:

        students = students.filter(
            student_class=selected_class
        )

    # ========================================================
    # STATUS FILTER
    # ========================================================

    if selected_status == "active":

        students = students.filter(
            is_active=True
        )

    elif selected_status == "inactive":

        students = students.filter(
            is_active=False
        )

    # ========================================================
    # COUNTS
    # ========================================================

    total_students = Student.objects.count()

    active_students = Student.objects.filter(
        is_active=True
    ).count()

    inactive_students = Student.objects.filter(
        is_active=False
    ).count()

    context = {

        "students": students,

        "search": search,

        "selected_class": selected_class,

        "selected_status": selected_status,

        "class_choices": Student.CLASS_CHOICES,

        "total_students": total_students,

        "active_students": active_students,

        "inactive_students": inactive_students,
    }

    return render(
        request,
        "dashboard/students.html",
        context
    )


# ============================================================
# STUDENT DETAIL
# ============================================================

@staff_member_required
def student_detail(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    # Get all payments belonging to this student

    payments = (
        Payment.objects
        .filter(
            student=student
        )
        .select_related(
            "fee_structure"
        )
        .order_by(
            "-transaction_date"
        )
    )

    # Calculate total paid

    total_paid = (
        payments
        .filter(
            status="VERIFIED"
        )
        .aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0")
    )

    context = {

        "student": student,

        "payments": payments,

        "total_paid": total_paid,
    }

    return render(
        request,
        "dashboard/student_detail.html",
        context
    )


# ============================================================
# ACTIVATE / DEACTIVATE STUDENT
# ============================================================

@staff_member_required
def toggle_student_status(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":

        student.is_active = not student.is_active

        student.save()

    return redirect(
        "dashboard:student_list"
    )


# ============================================================
# PAYMENTS
# ============================================================

@staff_member_required
def payment_list(request):

    payments = (
        Payment.objects
        .select_related(
            "student",
            "fee_structure",
        )
        .order_by(
            "-transaction_date"
        )
    )

    context = {

        "payments": payments,
    }

    return render(
        request,
        "dashboard/payments.html",
        context
    )


# ============================================================
# PAYMENT DETAIL
# ============================================================

@staff_member_required
def payment_detail(request, payment_id):

    payment = get_object_or_404(
        Payment.objects.select_related(
            "student",
            "fee_structure",
        ),
        id=payment_id
    )

    return render(
        request,
        "dashboard/payment_detail.html",
        {
            "payment": payment
        }
    )


# ============================================================
# DOWNLOAD PAYMENTS AS EXCEL
# ============================================================

@staff_member_required
def download_payments_excel(request):

    payments = (
        Payment.objects
        .select_related(
            "student",
            "fee_structure",
        )
        .order_by(
            "-transaction_date"
        )
    )

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Payments"

    # ========================================================
    # TITLE
    # ========================================================

    worksheet.merge_cells(
        "A1:H1"
    )

    worksheet["A1"] = (
        "ROCK FEE PORTAL - PAYMENT REPORT"
    )

    worksheet["A1"].font = Font(
        bold=True,
        size=16
    )

    worksheet["A1"].alignment = Alignment(
        horizontal="center"
    )

    # ========================================================
    # HEADERS
    # ========================================================

    headers = [

        "Payment Reference",

        "Student Name",

        "Student ID",

        "Class",

        "Payment Type",

        "Amount",

        "Status",

        "Transaction Date",
    ]

    for column_number, header in enumerate(
        headers,
        start=1
    ):

        cell = worksheet.cell(
            row=3,
            column=column_number
        )

        cell.value = header

        cell.font = Font(
            bold=True
        )

        cell.alignment = Alignment(
            horizontal="center"
        )

    # ========================================================
    # PAYMENT DATA
    # ========================================================

    row_number = 4

    for payment in payments:

        student = payment.student

        worksheet.cell(
            row=row_number,
            column=1
        ).value = payment.payment_reference

        worksheet.cell(
            row=row_number,
            column=2
        ).value = student.full_name

        worksheet.cell(
            row=row_number,
            column=3
        ).value = student.student_id

        worksheet.cell(
            row=row_number,
            column=4
        ).value = student.student_class

        worksheet.cell(
            row=row_number,
            column=5
        ).value = payment.get_payment_type_display()

        worksheet.cell(
            row=row_number,
            column=6
        ).value = float(
            payment.amount
        )

        worksheet.cell(
            row=row_number,
            column=7
        ).value = payment.status

        worksheet.cell(
            row=row_number,
            column=8
        ).value = payment.transaction_date

        row_number += 1

    # ========================================================
    # FORMAT DATA
    # ========================================================

    for row in worksheet.iter_rows(
        min_row=4,
        max_row=worksheet.max_row
    ):

        for cell in row:

            cell.alignment = Alignment(
                vertical="center"
            )

    # ========================================================
    # CURRENCY + DATE FORMATTING
    # ========================================================

    for row in range(
        4,
        worksheet.max_row + 1
    ):

        worksheet.cell(
            row=row,
            column=6
        ).number_format = '₦#,##0.00'

        worksheet.cell(
            row=row,
            column=8
        ).number_format = (
            "dd mmm yyyy hh:mm AM/PM"
        )

    # ========================================================
    # COLUMN WIDTHS
    # ========================================================

    column_widths = {

        "A": 25,

        "B": 28,

        "C": 18,

        "D": 15,

        "E": 22,

        "F": 18,

        "G": 15,

        "H": 25,
    }

    for column, width in column_widths.items():

        worksheet.column_dimensions[
            column
        ].width = width

    worksheet.freeze_panes = "A4"

    worksheet.auto_filter.ref = (
        f"A3:H{worksheet.max_row}"
    )

    # ========================================================
    # DOWNLOAD
    # ========================================================

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        )
    )

    response[
        "Content-Disposition"
    ] = (
        'attachment; '
        'filename="rock_fee_payments.xlsx"'
    )

    workbook.save(response)

    return response