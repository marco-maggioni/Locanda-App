from django.contrib import admin
from .models import Member

class MemberAdmin(admin.ModelAdmin):
  list_display = ("nome", "cognome", "email", "phone", "consenso", "invio", "mail_verificata", "iscrizione")

admin.site.register(Member, MemberAdmin)
