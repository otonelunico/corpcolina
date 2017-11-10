from django import forms


class ReqForm(forms.Form):

	class Meta:
		fields=[
            'dpts'
		]