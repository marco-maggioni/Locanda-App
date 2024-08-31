from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from .models import Member
from .forms import inputForm
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()
	
def form_view(request):
	if request.POST:
		form = inputForm(request.POST)
		if form.is_valid():
			member_mail = form.cleaned_data['email']
			member_name = form.cleaned_data['nome'].capitalize()
			mail_exist = Member.objects.filter(email=member_mail).exists() #controllo che la mail non sia gia presente nel db
			if not mail_exist: # se non è cosi:
				result = sendmail(member_name, member_mail) #invio la mail di controllo
				if result == 1: #se la mail viene inviata correttamente
					form.save() #salvo i dati nel database
					request.session['name'] = member_name
					request.session['email'] = member_mail
					return redirect(checking)
			else: #altrimenti ricarico la pagina con l'errore 
				my_error = 'Sembra che l\'email inserita sia già presente nel database.\nAggiungine una diversa per continuare.'
				context = {
					'form': form,
					'myerror' : my_error
				}
				return render(request, 'form.html', context)
	context = {
					'form': inputForm,
					'myerror' : ' '
				}
	return render(request, 'form.html', context)
	
def checking(request):
	return render(request, 'check.html', {'mail': request.session['email'],
									   'name': request.session['name'] })
	
def thanks_view(request, mail):
	memb = Member.objects.get(email=mail)
	memb.mail_verificata = True
	memb.save()
	return render(request, 'thanks.html')

def email_wrong(request):
	return HttpResponse('Something went wrong, please try later!')

def policy(request):
    return render(request, 'policy.html')

def sendmail(name, mail):
	sender_email = 'noreply.locanda@gmail.com'
	sender_psw = os.environ.get("SENDER_PSW")
	recipient_email = [mail]
	subject = "Locanda Mandelli - Conferma il tuo indirizzo di posta"
	page_url = "http://127.0.0.1:8000/locandaform/thankyou/" + str(mail) + "/"
	body = """\
	<html>
  		<body>
    		<p> Ciao """ + name + """,</p>
			<br>
      		Clicca <a href=""" + page_url + """>qui</a> per confermare la tua email.</p>
	  		<br>
    		<p>Oppure copia ed incolla il seguente link nel browser del tuo smartphone:</p>
			<p><u>http://127.0.0.1:8000/locandaform/thankyou/"""+ str(mail) + "/" +"""</u></p>
			<br>
    		<p>Ci sentiamo presto con le nostre novità!</p>
			<br>
			<p>Team Locanda Mandelli</p>
			<div>
				<footer>
					<small>Non rispondere a questo messaggio. Questa email è generata automaticamente dal nostro sistema.</small>
					<br>
					<small>Per ulteriori informazioni scrivi a:<a href="mailto:Locandamandelli@gmail.com"> Locandamandelli@gmail.com</a></small>
				</footer>
			</div>
  		</body>
	</html>
	"""
	try:
		html_message = MIMEText(body, 'html')
		html_message['Subject'] = subject
		html_message['From'] = sender_email
		html_message['To'] = " .".join(recipient_email)
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
			server.login(sender_email, sender_psw)
			server.sendmail(sender_email, recipient_email, html_message.as_string())
		result = 1
		return result
	except Exception as e:
		print('Something went wrong: ', e)
		return redirect(email_wrong)
	return