from django import forms

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
