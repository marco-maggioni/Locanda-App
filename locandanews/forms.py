# import form class from django
from typing import Any
from django import forms
# import GeeksModel from models.py
from .models import Member
 
# create a ModelForm
class inputForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
			#visible.field.widget.attrs['placeholder'] = visible.field.label
			
			self.fields['nome'].widget.attrs['placeholder'] = 'Nome'
			self.fields['cognome'].widget.attrs['placeholder'] = 'Cognome'
			self.fields['email'].widget.attrs['placeholder'] = 'Email'
			self.fields['phone'].widget.attrs['placeholder'] = 'Phone'
	
    # specify the name of model to use
	class Meta:
		model = Member
		fields = ["nome", "cognome", "email", "phone", 'consenso', 'invio']