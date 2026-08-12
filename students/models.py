from django.db import models
import uuid


class Student(models.Model):

    CLASS_CHOICES = [
        ("Primary 1", "Primary 1"),
        ("Primary 2", "Primary 2"),
        ("Primary 3", "Primary 3"),
        ("Primary 4", "Primary 4"),
        ("Primary 5", "Primary 5"),

        ("JSS 1", "JSS 1"),
        ("JSS 2", "JSS 2"),
        ("JSS 3", "JSS 3"),

        ("SSS 1", "SSS 1"),
        ("SSS 2", "SSS 2"),
        ("SSS 3", "SSS 3"),
    ]

    STUDENT_TYPE_CHOICES = [
        ("old", "Old Student"),
        ("new", "New Intake"),
    ]

    DEPARTMENT_CHOICES = [
        ("science", "Science"),
        ("art", "Art"),
    ]

    student_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    full_name = models.CharField(
        max_length=150
    )

    student_class = models.CharField(
        max_length=20,
        choices=CLASS_CHOICES
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

    parent_name = models.CharField(
        max_length=150
    )

    parent_phone = models.CharField(
        max_length=20
    )

    parent_email = models.EmailField()

    registered_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )


    def save(self, *args, **kwargs):

        # ====================================================
        # PRIMARY / JSS DO NOT HAVE DEPARTMENTS
        # ====================================================

        if not self.student_class.startswith("SSS"):

            self.department = None


        # ====================================================
        # GENERATE STUDENT ID
        # ====================================================

        if not self.student_id:

            self.student_id = (
                f"RFA-{uuid.uuid4().hex[:6].upper()}"
            )


        super().save(
            *args,
            **kwargs
        )


    def __str__(self):

        return (
            f"{self.student_id} - "
            f"{self.full_name}"
        )