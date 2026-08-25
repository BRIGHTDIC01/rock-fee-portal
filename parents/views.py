from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from students.models import Student
from fees.models import FeeStructure


# ============================================================
# PARENT REGISTER
# ============================================================

def parent_register(request):

    if request.user.is_authenticated:

        return redirect(
            "parent_dashboard"
        )

    if request.method == "POST":

        full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if not all([
            full_name,
            phone,
            email,
            username,
            password,
            confirm_password
        ]):

            messages.error(
                request,
                "Please fill in all fields."
            )

            return render(
                request,
                "parents/register.html"
            )

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "parents/register.html"
            )

        if User.objects.filter(
            username__iexact=username
        ).exists():

            messages.error(
                request,
                "That username is already taken."
            )

            return render(
                request,
                "parents/register.html"
            )

        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "An account with this email already exists."
            )

            return render(
                request,
                "parents/register.html"
            )

        # ----------------------------------------------------
        # CREATE USER + PARENT AS ONE TRANSACTION
        #
        # If anything fails while creating either record,
        # Django will automatically roll everything back.
        # This prevents incomplete accounts from being saved.
        # ----------------------------------------------------

        try:

            from parents.models import Parent

            with transaction.atomic():

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                Parent.objects.create(
                    user=user,
                    full_name=full_name,
                    phone=phone
                )

        except Exception:

            messages.error(
                request,
                "We could not create your account. Please check your details and try again."
            )

            return render(
                request,
                "parents/register.html"
            )

        # ----------------------------------------------------
        # LOGIN ONLY AFTER BOTH USER AND PARENT WERE CREATED
        # SUCCESSFULLY
        # ----------------------------------------------------

        login(
            request,
            user
        )

        return redirect(
            "parent_dashboard"
        )

    return render(
        request,
        "parents/register.html"
    )


# ============================================================
# HOW TO USE THE PARENT PORTAL
# ============================================================

def parent_guide(request):

    return render(
        request,
        "parents/guide.html"
    )

# ============================================================
# PARENT LOGIN
# ============================================================

def parent_login(request):

    if request.user.is_authenticated:

        return redirect(
            "parent_dashboard"
        )

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        if not username or not password:

            messages.error(
                request,
                "Please enter both your username and password."
            )

            return render(
                request,
                "parents/login.html"
            )

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user is None:

            messages.error(
                request,
                "Invalid username or password."
            )

            return render(
                request,
                "parents/login.html"
            )

        from parents.models import Parent

        try:

            parent = user.parent_profile

        except Parent.DoesNotExist:

            messages.error(
                request,
                "This account is not registered as a parent account."
            )

            return render(
                request,
                "parents/login.html"
            )

        if not parent.is_active:

            messages.error(
                request,
                "Your parent account has been deactivated."
            )

            return render(
                request,
                "parents/login.html"
            )

        login(
            request,
            user
        )

        return redirect(
            "parent_dashboard"
        )

    return render(
        request,
        "parents/login.html"
    )


# ============================================================
# PARENT DASHBOARD
# ============================================================

def parent_dashboard(request):

    if not request.user.is_authenticated:

        return redirect(
            "parent_login"
        )

    from parents.models import Parent

    try:

        parent = request.user.parent_profile

    except Parent.DoesNotExist:

        logout(request)

        messages.error(
            request,
            "Parent account not found."
        )

        return redirect(
            "parent_login"
        )

    if not parent.is_active:

        logout(request)

        messages.error(
            request,
            "Your parent account has been deactivated."
        )

        return redirect(
            "parent_login"
        )

    # --------------------------------------------------------
    # Get parent's students
    # --------------------------------------------------------

    students = list(
        parent.students.all()
    )

    # --------------------------------------------------------
    # Find EXACT current fee for every student
    # --------------------------------------------------------

    for student in students:

        student.current_fee = None

        fee_query = FeeStructure.objects.filter(
            session__is_active=True,
            student_class=student.student_class,
            student_type=student.student_type,
        )

        # SSS = department matters
        if student.student_class.startswith("SSS"):

            fee_query = fee_query.filter(
                department=student.department
            )

        # Other classes = no department
        else:

            fee_query = fee_query.filter(
                department__isnull=True
            )

        student.current_fee = (
            fee_query
            .select_related(
                "session",
                "term"
            )
            .order_by(
                "-created_at"
            )
            .first()
        )

    return render(
        request,
        "parents/dashboard.html",
        {
            "parent": parent,
            "students": students,
        }
    )


# ============================================================
# ADD STUDENT
# ============================================================

def add_student(request):

    if not request.user.is_authenticated:

        return redirect(
            "parent_login"
        )

    from parents.models import Parent

    try:

        parent = request.user.parent_profile

    except Parent.DoesNotExist:

        logout(request)

        messages.error(
            request,
            "Parent account not found."
        )

        return redirect(
            "parent_login"
        )

    if not parent.is_active:

        logout(request)

        messages.error(
            request,
            "Your parent account has been deactivated."
        )

        return redirect(
            "parent_login"
        )

    if request.method == "POST":

        full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        student_class = request.POST.get(
            "student_class",
            ""
        ).strip()

        student_type = request.POST.get(
            "student_type",
            ""
        ).strip()

        department = request.POST.get(
            "department",
            ""
        ).strip()

        if not full_name:

            messages.error(
                request,
                "Please enter the student's full name."
            )

            return render(
                request,
                "parents/add_student.html"
            )

        valid_classes = [

            "Primary 1",
            "Primary 2",
            "Primary 3",
            "Primary 4",
            "Primary 5",

            "JSS 1",
            "JSS 2",
            "JSS 3",

            "SSS 1",
            "SSS 2",
            "SSS 3",
        ]

        if student_class not in valid_classes:

            messages.error(
                request,
                "Please select a valid class."
            )

            return render(
                request,
                "parents/add_student.html"
            )

        if student_type not in [
            "old",
            "new"
        ]:

            messages.error(
                request,
                "Please select the student's type."
            )

            return render(
                request,
                "parents/add_student.html"
            )

        if student_class.startswith("SSS"):

            if department not in [
                "science",
                "art"
            ]:

                messages.error(
                    request,
                    "Please select Science or Art for SSS students."
                )

                return render(
                    request,
                    "parents/add_student.html"
                )

        else:

            department = None

        student = Student.objects.create(

            full_name=full_name,

            student_class=student_class,

            student_type=student_type,

            department=department,

            parent_name=parent.full_name,

            parent_phone=parent.phone,

            parent_email=parent.user.email
        )

        parent.students.add(
            student
        )

        messages.success(
            request,
            f"{student.full_name} has been added successfully."
        )

        return redirect(
            "parent_dashboard"
        )

    return render(
        request,
        "parents/add_student.html"
    )


# ============================================================
# LOGOUT
# ============================================================

def parent_logout(request):

    logout(request)

    return redirect(
        "parent_login"
    )