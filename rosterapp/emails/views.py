from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

def test_email(request):

	if request.method=='POST':
		message = request.POST['message']
		send_mail(
    		'Test Mail 1 ',
    		message,
    		'settings.EMAIL_HOST_USER',
    		['levitegpeter@gmail.com'],
    		fail_silently=False,
		)
		
	return render(request,'emails/test.html')

def test_cron():

	message = "TESTING CRON"
	send_mail(
    	'CRON SCHEDULE ',
    	message,
    	'settings.EMAIL_HOST_USER',
    	['levitegpeter@gmail.com'],
    	fail_silently=False,
	)
		
	return 
