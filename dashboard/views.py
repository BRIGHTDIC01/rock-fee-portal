from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import render

from fees.models import AcademicSession, FeeStructure, Payment
from parents.models import Parent
from students.models import Student


@staff_member_required
def dashboard(request):

    # ========================================================
    # BASIC COUNTS
    # ========================================================

    total_students = Student.objects.filter(
        is_active=True
    ).count()

    total_parents = Parent.objects.filter(
        is_active=True
    ).count()

    total_fee_structures = FeeStructure.objects.count()

    # ========================================================
    # ACTIVE ACADEMIC SESSION
    # ========================================================

    active_session = AcademicSession.objects.filter(
        is_active=True
    ).first()

    # ========================================================
    # PAYMENT STATISTICS
    # ========================================================

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

    # ========================================================
    # EXPECTED FEES
    # ========================================================

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

            # SSS students require department
            if student.student_class.startswith("SSS"):

                fee_query = fee_query.filter(
                    department=student.department
                )

            # Primary/JSS students do not
            else:

                fee_query = fee_query.filter(
                    department__isnull=True
                )

            fee = fee_query.first()

            if fee:

                expected_fees += fee.total_fee

    # ========================================================
    # OUTSTANDING
    # ========================================================

    outstanding = expected_fees - total_collected

    if outstanding < 0:
        outstanding = Decimal("0")

    # ========================================================
    # RECENT PAYMENTS
    # ========================================================

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

    # ========================================================
    # CONTEXT
    # ========================================================

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