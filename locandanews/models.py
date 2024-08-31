from django.db import models
from datetime import date

class Member(models.Model):
	nome = models.CharField(max_length=50)
	cognome = models.CharField(max_length=50)
	email = models.EmailField(max_length=254)
	phone = models.CharField(max_length=60, null=True, blank=True) #https://stackoverflow.com/questions/59480134/how-to-store-a-phone-number-django
	consenso = models.BooleanField(null=False, blank=False)
	invio = models.BooleanField(null=False, blank=False)
	mail_verificata = models.BooleanField(default=False)
	iscrizione = models.DateField(default=date.today) #https://stackoverflow.com/questions/76383841/how-to-set-the-current-proper-date-and-time-to-datefield-and-timefield-r
	title = models.CharField(max_length=30, null=True)
	
	def __str__(self):
		return self.title or ''