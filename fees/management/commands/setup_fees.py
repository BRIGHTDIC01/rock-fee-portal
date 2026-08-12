from django.core.management.base import BaseCommand

from fees.models import AcademicSession, Term, FeeStructure


class Command(BaseCommand):

    help = "Create Rock Foundation academic session, term and school fees."

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.WARNING(
                "Setting up Rock Foundation school fees..."
            )
        )

        # --------------------------------------------------
        # ACADEMIC SESSION
        # --------------------------------------------------

        session, created = AcademicSession.objects.get_or_create(
            name="2026/2027",
            defaults={
                "is_active": True
            }
        )

        # Make sure this session is active
        if not session.is_active:
            session.is_active = True
            session.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    "Created Academic Session: 2026/2027"
                )
            )
        else:
            self.stdout.write(
                "Academic Session 2026/2027 already exists."
            )

        # --------------------------------------------------
        # TERM
        # --------------------------------------------------

        term, created = Term.objects.get_or_create(
            name="First Term"
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    "Created Term: First Term"
                )
            )
        else:
            self.stdout.write(
                "Term First Term already exists."
            )

        # --------------------------------------------------
        # SCHOOL FEES
        # --------------------------------------------------

        fees = [

            # =========================
            # PRIMARY
            # =========================

            {
                "student_class": "Primary 1",
                "student_type": "old",
                "department": None,
                "amount": 31800,
            },

            {
                "student_class": "Primary 1",
                "student_type": "new",
                "department": None,
                "amount": 40300,
            },

            {
                "student_class": "Primary 2",
                "student_type": "old",
                "department": None,
                "amount": 31800,
            },

            {
                "student_class": "Primary 2",
                "student_type": "new",
                "department": None,
                "amount": 40300,
            },

            {
                "student_class": "Primary 3",
                "student_type": "old",
                "department": None,
                "amount": 38800,
            },

            {
                "student_class": "Primary 3",
                "student_type": "new",
                "department": None,
                "amount": 47300,
            },

            {
                "student_class": "Primary 4",
                "student_type": "old",
                "department": None,
                "amount": 38800,
            },

            {
                "student_class": "Primary 4",
                "student_type": "new",
                "department": None,
                "amount": 47300,
            },

            {
                "student_class": "Primary 5",
                "student_type": "old",
                "department": None,
                "amount": 38800,
            },

            {
                "student_class": "Primary 5",
                "student_type": "new",
                "department": None,
                "amount": 47300,
            },


            # =========================
            # JSS
            # =========================

            {
                "student_class": "JSS 1",
                "student_type": "old",
                "department": None,
                "amount": 48300,
            },

            {
                "student_class": "JSS 1",
                "student_type": "new",
                "department": None,
                "amount": 48300,
            },

            {
                "student_class": "JSS 2",
                "student_type": "old",
                "department": None,
                "amount": 39800,
            },

            {
                "student_class": "JSS 2",
                "student_type": "new",
                "department": None,
                "amount": 48300,
            },

            {
                "student_class": "JSS 3",
                "student_type": "old",
                "department": None,
                "amount": 41800,
            },

            {
                "student_class": "JSS 3",
                "student_type": "new",
                "department": None,
                "amount": 50300,
            },


            # =========================
            # SSS 1 SCIENCE
            # =========================

            {
                "student_class": "SSS 1",
                "student_type": "old",
                "department": "science",
                "amount": 46800,
            },

            {
                "student_class": "SSS 1",
                "student_type": "new",
                "department": "science",
                "amount": 55300,
            },


            # =========================
            # SSS 1 ART
            # =========================

            {
                "student_class": "SSS 1",
                "student_type": "old",
                "department": "art",
                "amount": 43800,
            },

            {
                "student_class": "SSS 1",
                "student_type": "new",
                "department": "art",
                "amount": 52300,
            },


            # =========================
            # SSS 2 SCIENCE
            # =========================

            {
                "student_class": "SSS 2",
                "student_type": "old",
                "department": "science",
                "amount": 46800,
            },

            {
                "student_class": "SSS 2",
                "student_type": "new",
                "department": "science",
                "amount": 55300,
            },


            # =========================
            # SSS 2 ART
            # =========================

            {
                "student_class": "SSS 2",
                "student_type": "old",
                "department": "art",
                "amount": 43800,
            },

            {
                "student_class": "SSS 2",
                "student_type": "new",
                "department": "art",
                "amount": 52300,
            },


            # =========================
            # SSS 3 SCIENCE
            # =========================

            {
                "student_class": "SSS 3",
                "student_type": "old",
                "department": "science",
                "amount": 52800,
            },

            {
                "student_class": "SSS 3",
                "student_type": "new",
                "department": "science",
                "amount": 61300,
            },


            # =========================
            # SSS 3 ART
            # =========================

            {
                "student_class": "SSS 3",
                "student_type": "old",
                "department": "art",
                "amount": 48800,
            },

            {
                "student_class": "SSS 3",
                "student_type": "new",
                "department": "art",
                "amount": 57300,
            },
        ]

        # --------------------------------------------------
        # CREATE FEE STRUCTURES
        # --------------------------------------------------

        created_count = 0

        for fee in fees:

            fee_structure, created = FeeStructure.objects.get_or_create(

                session=session,

                term=term,

                student_class=fee["student_class"],

                student_type=fee["student_type"],

                department=fee["department"],

                defaults={
                    "total_fee": fee["amount"]
                }
            )

            # If it already exists, make sure
            # the amount is correct.

            if not created:

                if fee_structure.total_fee != fee["amount"]:

                    fee_structure.total_fee = fee["amount"]

                    fee_structure.save(
                        update_fields=["total_fee"]
                    )

            else:

                created_count += 1

        # --------------------------------------------------
        # FINISHED
        # --------------------------------------------------

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                " ROCK FOUNDATION FEES SET UP SUCCESSFULLY"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write(
            f"Academic Session: {session.name}"
        )

        self.stdout.write(
            f"Term: {term.name}"
        )

        self.stdout.write(
            f"Fee structures created: {created_count}"
        )

        self.stdout.write(
            f"Total fee structures: {FeeStructure.objects.filter(session=session, term=term).count()}"
        )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "You can now use these fees in the parent portal."
            )
        )