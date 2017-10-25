from django import forms

from .models import Ticket, Establecimiento, Tema, Respuestas, Tecnico

class TicketForm(forms.ModelForm):

	class Meta:
		model=Ticket
		fields=[
			'tema',
			'establecimiento',
			'nom_contacto',
			'ape_contacto',
			'correo_contacto',
			'fijo_contacto',
			'celu_contacto',
			'resum_problema',
			'asignado',
			'detall_problema',
			'estado',
		]
		"""
		labels={
			'tema':'Tema',
			'establecimiento':'Establecimiento',
			'nom_contacto':'Nom_contacto',
			'ape_contacto':'Ape_contacto',
			'correo_contacto':'Correo_contacto',
			'fijo_contacto':'Fijo_contacto',
			'celu_contacto':'Celu_contacto',
			'resum_problema':'Resum_problema',
			'asignado':'Asignado',
			'detall_problema':'Detall_problema',
			'estado':'Estado',
		}
		widgets={
			'tema': forms.Select(attrs={'class':'form-control'}),
			'establecimiento': forms.Select(attrs={'class':'form-control' }),
			'nom_contacto': forms.TextInput(attrs={'class':'form-control'}),
			'ape_contacto': forms.TextInput(attrs={'class':'form-control'}),
			'correo_contacto': forms.TextInput(attrs={'class':'form-control'}),
			'fijo_contacto': forms.TextInput(attrs={'class':'form-control'}),
			'celu_contacto': forms.TextInput(attrs={'class':'form-control'}),
			'resum_problema': forms.TextInput(attrs={'class':'form-control'}),
			'asignado': forms.Select(attrs={'class':'form-control'}),
			'detall_problema': forms.Textarea(attrs={'class':'form-control'}),
			'estado': forms.Select(attrs={'class':'form-control'}),
		} """

class EstablecimientoForm(forms.ModelForm):

	class Meta:
		model = Establecimiento
		fields = [
			'titulo',
		]
		labels = {
			'titulo':'Titulo',

		}
		widgets = {
			'titulo': forms.TextInput(attrs={'class':'form-control'}),

		}

class TemaForm(forms.ModelForm):

	class Meta:
		model = Tema
		fields = [
			'titulo',
		]
		labels = {
			'titulo':'Titulo',

		}
		widgets = {
			'titulo': forms.TextInput(attrs={'class':'form-control'}),

		}

class RespuestaForm(forms.ModelForm):

	class Meta:
		model = Respuestas
		fields = [
            'mensaje' ,
		]
		"""
		labels = {
            'asunto': 'Asunto',
            'mensaje': 'Mensaje',
		}
		widgets = {
            'asunto': forms.TextInput(attrs={'class':'form-control'}),
            'mensaje': forms.Textarea(attrs={'class':'form-control'}),
		}"""

class TecnicoForm(forms.ModelForm):

	class Meta:
		model=Tecnico
		fields = [
			'nombre',
			'apellido',
			'correo',
			]
		labels = {
			'nombre':'Nombre',
			'apellido':'Apellido',
			'correo':'Correo',
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'apellido': forms.TextInput(attrs={'class':'form-control'}),
			'correo': forms.TextInput(attrs={'class':'form-control'}),
		}
