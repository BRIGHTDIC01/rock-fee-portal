from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import (
    AcademicSession,
    Term,
    FeeStructure,
    Payment,
)


# ============================================================
# ACADEMIC SESSION
# ============================================================

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "-is_active",
        "-created_at",
    )


# ============================================================
# TERM
# ============================================================

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# ============================================================
# FEE STRUCTURE
# ============================================================

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):

    list_display = (
        "session",
        "term",
        "student_class",
        "student_type_display",
        "department_display",
        "formatted_fee",
        "payment_deadline",
        "created_at",
    )

    list_filter = (
        "session",
        "term",
        "student_class",
        "student_type",
        "department",
    )

    search_fields = (
        "student_class",
        "student_type",
        "department",
    )

    ordering = (
        "student_class",
        "student_type",
        "department",
    )

    # --------------------------------------------------------
    # ADMIN FORM
    # --------------------------------------------------------

    fieldsets = (

        (
            "Fee Configuration",
            {
                "fields": (
                    "session",
                    "term",
                    "student_class",
                    "student_type",
                    "department",
                    "total_fee",
                    "payment_deadline",
                )
            },
        ),

    )

    # --------------------------------------------------------
    # DISPLAY STUDENT TYPE
    # --------------------------------------------------------

    @admin.display(
        description="Student Type",
        ordering="student_type",
    )
    def student_type_display(self, obj):

        return obj.get_student_type_display()

    # --------------------------------------------------------
    # DISPLAY DEPARTMENT
    # --------------------------------------------------------

    @admin.display(
        description="Department",
        ordering="department",
    )
    def department_display(self, obj):

        if obj.department:

            return obj.get_department_display()

        return "—"

    # --------------------------------------------------------
    # DISPLAY FEE
    # --------------------------------------------------------

    @admin.display(
        description="School Fee",
        ordering="total_fee",
    )
    def formatted_fee(self, obj):

        return f"₦{obj.total_fee:,.0f}"


# ============================================================
# PAYMENT
# ============================================================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "payment_reference",
        "student",
        "fee_structure",
        "payment_type",
        "display_amount",
        "status",
        "transaction_date",
        "verified_at",
    )

    list_filter = (
        "status",
        "payment_type",
        "transaction_date",
    )

    search_fields = (
        "payment_reference",
        "student__student_id",
        "student__full_name",
    )

    readonly_fields = (
        "payment_reference",
        "transaction_date",
        "verified_at",
        "payment_proof_preview",
    )

    fieldsets = (

        (
            "Payment Information",
            {
                "fields": (
                    "payment_reference",
                    "student",
                    "fee_structure",
                    "payment_type",
                    "amount",
                )
            },
        ),

        (
            "Payment Proof",
            {
                "fields": (
                    "payment_proof",
                    "payment_proof_preview",
                )
            },
        ),

        (
            "Verification",
            {
                "fields": (
                    "status",
                    "verified_at",
                )
            },
        ),

        (
            "Transaction",
            {
                "fields": (
                    "transaction_date",
                )
            },
        ),

    )

    # --------------------------------------------------------
    # DISPLAY PAYMENT AMOUNT
    # --------------------------------------------------------

    @admin.display(
        description="Amount"
    )
    def display_amount(self, obj):

        return f"₦{obj.amount:,.0f}"

    # --------------------------------------------------------
    # PAYMENT PROOF PREVIEW
    # --------------------------------------------------------

    @admin.display(
        description="Receipt Preview"
    )
    def payment_proof_preview(self, obj):

        if obj.payment_proof:

            return format_html(
                '<img src="{}" '
                'style="max-width:500px; '
                'max-height:500px; '
                'border-radius:10px; '
                'object-fit:contain;" />',
                obj.payment_proof.url
            )

        return "No payment proof uploaded."

    # --------------------------------------------------------
    # SAVE PAYMENT
    # --------------------------------------------------------

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        if obj.status == "VERIFIED":

            if not obj.verified_at:

                obj.verified_at = timezone.now()

        else:

            obj.verified_at = None

        super().save_model(
            request,
            obj,
            form,
            change
        )