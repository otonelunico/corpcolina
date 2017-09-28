from django import forms
from documents.models import Document, Receiver, Remittent

class DocumentForm(forms.ModelForm):

	class Meta:
		model=Document
		fields=[
			'type',
			'matter',
			'remittent',
			'receiver',
			'body',
			'footer',
			'change'
		]
		labels={
			'type':'Type',
			'matter':'Matter',
			'remittent':'Remittent',
			'receiver':'Receiver',
			'body':'Body',
			'footer':'Footer',
			'change':'Change'
		}
		widgets={
			'type':forms.Select(attrs={'class':'form-control'}),
			'matter': forms.TextInput(attrs={'class':'form-control'}),
			'remittent': forms.Select(attrs={'class':'form-control'}),
			'receiver': forms.Select(attrs={'class':'form-control'}),
			'body': forms.Textarea(attrs={'class':'form-control'}),
			'footer': forms.Textarea(attrs={'class':'form-control'}),
			'change':forms.CheckboxInput(attrs={'class':'form-control'}),
			}

class RemittentForm(forms.ModelForm):

	class Meta:
		model = Remittent
		fields = [
			'last_name',
			'first_name',
			'job_title',
			'signature'
		]
		labels = {
			'last_name':'Last_name',
			'first_name':'First_name',
			'job_title':'Job_title',
			'signature': 'Signature',

		}
		widgets = {
			'last_name': forms.TextInput(attrs={'class':'form-control'}),
			'first_name': forms.TextInput(attrs={'class':'form-control'}),
			'job_title': forms.TextInput(attrs={'class':'form-control'}),
			'firsignaturema': forms.Textarea(attrs={'class':'form-control'}),

		}


class ReceiverForm(forms.ModelForm):

	class Meta:
		model = Receiver
		fields = [
			'last_name',
			'first_name',
			'job_title',
		]
		labels = {
			'last_name': 'Last_name',
			'first_name': 'First_name',
			'job_title': 'Job_title',

		}
		widgets = {
			'last_name': forms.TextInput(attrs={'class': 'form-control'}),
			'first_name': forms.TextInput(attrs={'class': 'form-control'}),
			'job_title': forms.TextInput(attrs={'class': 'form-control'}),
		}
