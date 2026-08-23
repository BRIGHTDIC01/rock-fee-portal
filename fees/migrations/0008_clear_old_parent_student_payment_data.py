from django.db import migrations


def clear_old_portal_records(apps, schema_editor):
    """
    One-time cleanup for the old portal records.

    This intentionally removes:
      - all Payment records
      - all Parent records (and their parent user accounts via CASCADE)
      - all Student records

    It does NOT remove fee structures, academic sessions, terms, or staff/admin users.
    """
    Payment = apps.get_model("fees", "Payment")
    Parent = apps.get_model("parents", "Parent")
    Student = apps.get_model("students", "Student")

    Payment.objects.all().delete()
    Parent.objects.all().delete()
    Student.objects.all().delete()


def reverse_cleanup(apps, schema_editor):
    # The deleted records cannot be reconstructed safely from a migration.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("fees", "0007_alter_payment_payment_type"),
        ("parents", "0001_initial"),
        ("students", "0002_student_department_student_student_type"),
    ]

    operations = [
        migrations.RunPython(clear_old_portal_records, reverse_cleanup),
    ]
