from django import forms
from department.models import departament

class DesdeForm(forms.ModelForm):

	class Meta:
		model = departament
		fields = [
			'name',
			'description',
		]
		labels = {
			'name':'Name',
			'description':'Description',

		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'description': forms.TextInput(attrs={'class':'form-control'}),

		}
