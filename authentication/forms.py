from django import forms
from authentication.models import Logeado, Transfer



class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = (
            'transfer',
        )
