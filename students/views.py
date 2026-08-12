from django.shortcuts import render
from django.contrib import messages

from .models import Student


def register_student(request):

    if request.method == "POST":

        full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        student_class = request.POST.get(
            "student_class",
            ""
        )

        parent_name = request.POST.get(
            "parent_name",
            ""
        ).strip()

        parent_phone = request.POST.get(
            "parent_phone",
            ""
        ).strip()

        parent_email = request.POST.get(
            "parent_email",
            ""
        ).strip()

        # Check required fields
        if not all([
            full_name,
            student_class,
            parent_name,
            parent_phone,
            parent_email,
        ]):

            messages.error(
                request,
                "Please fill in all the required fields."
            )

            return render(
                request,
                "students/register.html"
            )

        # Prevent exact duplicate
        duplicate = Student.objects.filter(
            full_name__iexact=full_name,
            student_class=student_class,
        ).exists()

        if duplicate:

            messages.error(
                request,
                "A student with this exact name is already registered in this class."
            )

            return render(
                request,
                "students/register.html"
            )

        # Create student
        student = Student.objects.create(
            full_name=full_name,
            student_class=student_class,
            parent_name=parent_name,
            parent_phone=parent_phone,
            parent_email=parent_email,
        )

        return render(
            request,
            "students/registration_success.html",
            {
                "student": student,
            },
        )

    return render(
        request,
        "students/register.html"
    )


def student_portal(request):

    student_id = request.GET.get(
        "student_id",
        ""
    ).strip()

    student = None

    if student_id:

        try:
            student = Student.objects.get(
                student_id=student_id
            )

        except Student.DoesNotExist:

            messages.error(
                request,
                "Student ID not found."
            )

    return render(
        request,
        "students/portal.html",
        {
            "student": student,
        },
    )