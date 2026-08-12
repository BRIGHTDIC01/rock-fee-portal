from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

from students.models import Student


class AcademicSession(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True
    )

    is_active = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if self.is_active:

            AcademicSession.objects.exclude(
                pk=self.pk
            ).update(
                is_active=False
            )

        super().save(*args, **kwargs)


class Term(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class FeeStructure(models.Model):

    STUDENT_TYPE_CHOICES = [
        ("old", "Old Student"),
        ("new", "New Intake"),
    ]

    DEPARTMENT_CHOICES = [
        ("science", "Science"),
        ("art", "Art"),
    ]

    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name="fee_structures"
    )

    term = models.ForeignKey(
        Term,
        on_delete=models.CASCADE,
        related_name="fee_structures"
    )

    student_class = models.CharField(
        max_length=50
    )

    student_type = models.CharField(
        max_length=10,
        choices=STUDENT_TYPE_CHOICES,
        default="old"
    )

    department = models.CharField(
        max_length=10,
        choices=DEPARTMENT_CHOICES,
        blank=True,
        null=True
    )

    total_fee = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    payment_deadline = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "student_class",
            "student_type",
            "department",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "session",
                    "term",
                    "student_class",
                    "student_type",
                    "department",
                ],
                name="unique_fee_structure"
            )
        ]

    def __str__(self):

        department = ""

        if self.department:
            department = (
                f" - {self.get_department_display()}"
            )

        return (
            f"{self.student_class}"
            f"{department}"
            f" - {self.get_student_type_display()}"
            f" - ₦{self.total_fee:,.0f}"
        )

    @property
    def seventy_five_percent(self):

        return (
            self.total_fee *
            75 /
            100
        )

    @property
    def twenty_five_percent(self):

        return (
            self.total_fee *
            25 /
            100
        )


class Payment(models.Model):

    PAYMENT_TYPE_CHOICES = [
        ("FULL", "Full Payment"),
        ("75", "75% Payment"),
        ("25", "25% Payment"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("VERIFIED", "Verified"),
        ("REJECTED", "Rejected"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    fee_structure = models.ForeignKey(
        FeeStructure,
        on_delete=models.PROTECT,
        related_name="payments"
    )

    payment_reference = models.CharField(
        max_length=30,
        unique=True,
        editable=False
    )

    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_TYPE_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    payment_proof = models.FileField(
        upload_to="payment_proofs/"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    transaction_date = models.DateTimeField(
        default=timezone.now
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        if not self.payment_reference:

            import uuid

            self.payment_reference = (
                "ROCK-"
                + uuid.uuid4().hex[:10].upper()
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.payment_reference