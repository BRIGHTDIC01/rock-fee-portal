from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template

from xhtml2pdf import pisa

from .forms import PaymentForm
from .models import Payment, Student, FeeStructure


@login_required
def make_payment(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    # Get the currently active fee structure
    fee_structure = (
        FeeStructure.objects
        .filter(
            session__is_active=True,
            student_class=student.student_class,
        )
        .select_related(
            "session",
            "term",
        )
        .order_by(
            "-session__created_at"
        )
        .first()
    )

    # No fee structure found
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

    # POST = submit payment
    if request.method == "POST":

        form = PaymentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            payment = form.save(
                commit=False
            )

            payment.student = student

            payment.fee_structure = fee_structure

            payment.status = "PENDING"

            payment.save()

            return redirect(
                "receipt",
                payment_id=payment.id
            )

    else:

        form = PaymentForm()

    return render(
        request,
        "fees/make_payment.html",
        {
            "student": student,
            "fee_structure": fee_structure,
            "form": form,
        }
    )


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