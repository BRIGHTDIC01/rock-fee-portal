from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.template.loader import get_template

from xhtml2pdf import pisa

from .forms import PaymentForm
from .models import Payment, FeeStructure

from students.models import Student
from parents.models import Parent


# ============================================================
# MAKE PAYMENT
# FULL PAYMENT ONLY
# ============================================================

@login_required
def make_payment(request, student_id):

    # --------------------------------------------------------
    # GET LOGGED-IN PARENT
    # --------------------------------------------------------

    try:

        parent = request.user.parent_profile

    except Parent.DoesNotExist:

        return redirect(
            "parent_login"
        )

    # --------------------------------------------------------
    # GET STUDENT
    # --------------------------------------------------------

    student = get_object_or_404(
        Student,
        id=student_id
    )

    # --------------------------------------------------------
    # SECURITY CHECK
    #
    # Student has a MANY-TO-MANY relationship with parents.
    # Make sure this student belongs to this parent.
    # --------------------------------------------------------

    if not parent.students.filter(
        id=student.id
    ).exists():

        return redirect(
            "parent_dashboard"
        )

    # --------------------------------------------------------
    # FIND EXACT CURRENT FEE
    #
    # Match:
    #   ACTIVE SESSION
    #   STUDENT CLASS
    #   STUDENT TYPE
    #   DEPARTMENT
    # --------------------------------------------------------

    fee_query = FeeStructure.objects.filter(

        session__is_active=True,

        student_class=student.student_class,

        student_type=student.student_type

    )

    # --------------------------------------------------------
    # SSS STUDENTS
    # --------------------------------------------------------

    if student.student_class.startswith("SSS"):

        fee_query = fee_query.filter(
            department=student.department
        )

    # --------------------------------------------------------
    # NON-SSS STUDENTS
    # --------------------------------------------------------

    else:

        fee_query = fee_query.filter(
            department__isnull=True
        )

    # --------------------------------------------------------
    # GET EXACT FEE
    # --------------------------------------------------------

    fee_structure = (
        fee_query
        .select_related(
            "session",
            "term",
        )
        .order_by(
            "-created_at"
        )
        .first()
    )

    # --------------------------------------------------------
    # NO FEE FOUND
    # --------------------------------------------------------

    if not fee_structure:

        return render(
            request,
            "fees/make_payment.html",
            {
                "student": student,
                "fee_structure": None,
                "form": PaymentForm(),
                "no_fee": True,
            }
        )

    # --------------------------------------------------------
    # POST PAYMENT
    # --------------------------------------------------------

    if request.method == "POST":

        form = PaymentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            amount = form.cleaned_data["amount"]

            # ------------------------------------------------
            # FULL PAYMENT MUST EQUAL EXACT FEE
            # ------------------------------------------------

            if amount != fee_structure.total_fee:

                form.add_error(
                    "amount",
                    (
                        "Full payment must be exactly "
                        f"₦{fee_structure.total_fee:,.0f}."
                    )
                )

            else:

                payment = form.save(
                    commit=False
                )

                payment.student = student

                payment.fee_structure = fee_structure

                payment.payment_type = "FULL"

                payment.amount = fee_structure.total_fee

                payment.status = "PENDING"

                payment.save()

                return redirect(
                    "receipt",
                    payment_id=payment.id
                )

    else:

        form = PaymentForm(
            initial={
                "amount": fee_structure.total_fee
            }
        )

    # --------------------------------------------------------
    # RENDER PAYMENT PAGE
    # --------------------------------------------------------

    return render(
        request,
        "fees/make_payment.html",
        {
            "student": student,
            "fee_structure": fee_structure,
            "form": form,
        }
    )


# ============================================================
# RECEIPT
# ============================================================

@login_required
def receipt(request, payment_id):

    payment = get_object_or_404(
        Payment.objects.select_related(
            "student",
            "fee_structure",
            "fee_structure__session",
            "fee_structure__term",
        ),
        id=payment_id,
    )

    return render(
        request,
        "fees/receipt.html",
        {
            "payment": payment,
        }
    )


# ============================================================
# DOWNLOAD RECEIPT
# ============================================================

@login_required
def download_receipt(request, payment_id):

    payment = get_object_or_404(
        Payment.objects.select_related(
            "student",
            "fee_structure",
            "fee_structure__session",
            "fee_structure__term",
        ),
        id=payment_id,
    )

    template = get_template(
        "fees/receipt_pdf.html"
    )

    html = template.render(
        {
            "payment": payment,
            "request": request,
        }
    )

    result = BytesIO()

    pdf = pisa.pisaDocument(
        BytesIO(
            html.encode("UTF-8")
        ),
        result,
    )

    if pdf.err:

        return HttpResponse(
            "Sorry, there was an error generating your receipt.",
            status=500,
        )

    response = HttpResponse(
        result.getvalue(),
        content_type="application/pdf",
    )

    filename = (
        "Rock-Foundation-Receipt-"
        f"{payment.payment_reference}.pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response