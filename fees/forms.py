from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment

        fields = [
            "payment_type",
            "amount",
            "payment_proof",
        ]

        widgets = {
            "payment_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter payment amount",
                    "min": "1",
                    "step": "1",
                }
            ),

            "payment_proof": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".jpg,.jpeg,.png,.pdf",
                }
            ),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        if amount is None:
            raise forms.ValidationError(
                "Please enter the payment amount."
            )

        if amount <= 0:
            raise forms.ValidationError(
                "Payment amount must be greater than ₦0."
            )

        return amount

    def clean_payment_proof(self):
        payment_proof = self.cleaned_data.get("payment_proof")

        if not payment_proof:
            raise forms.ValidationError(
                "Please upload your payment proof."
            )

        allowed_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".pdf",
        ]

        filename = payment_proof.name.lower()

        if not any(
            filename.endswith(extension)
            for extension in allowed_extensions
        ):
            raise forms.ValidationError(
                "Please upload a JPG, JPEG, PNG or PDF file."
            )

        max_size = 5 * 1024 * 1024

        if payment_proof.size > max_size:
            raise forms.ValidationError(
                "Payment proof must not exceed 5 MB."
            )

        return payment_proof