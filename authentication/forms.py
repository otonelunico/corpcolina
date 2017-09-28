from django import forms
from authentication.models import Logeado

class DeptoForm(forms.ModelForm):

	class Meta:
		model = Logeado
		fields = [
			'departament',
		]
		labels = {
			'departament':'Departament',

		}
		widgets = {
			'departament': forms.TextInput(attrs={'class':'form-control'}),

		}
