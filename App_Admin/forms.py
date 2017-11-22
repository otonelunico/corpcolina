from django import forms


class ReqForm(forms.Form):
    user = forms.CharField(max_length=10)
    docs = forms.BooleanField()
    tick = forms.BooleanField()
    dpts = forms.CharField(max_length=100)
    coment = forms.Textarea()