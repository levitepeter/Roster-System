from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,get_user_model
User = get_user_model()

from django.contrib import messages, auth
from events.models import Event,Availability,FinalRoster
from datetime import date, datetime, timedelta
from .choices import month_choices
import calendar
# Create your views here.
from django.http import HttpResponse
def login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
			
		user=auth.authenticate(email=email,password=password)
		
		if user is not None:
			auth.login(request,user)
			if user.is_teamadmin:
				return redirect('adminpage')
			else:
				request.session['the_id'] = user.pk
				return redirect('availability')
		else:
			messages.error(request, 'Invalid credentials, user does not exist')
			return redirect('login')
	else:
		return render(request,'accounts/login.html')


def logout_view(request):
    auth.logout(request)
    return redirect('homepage')

def homepage(request):
	return render(request,'accounts/homepage.html')


def adminpage(request):
	context={
	'month_choices' : month_choices,
	}
	return render(request,'accounts/adminpage.html',context)

def availability(request):
	Events = Event.objects.all()
	latest_month = Event.objects.latest('event_date').event_date.month
	events_for_month = Event.objects.filter(event_date__month=latest_month)
	_dates = events_for_month.values_list('event_date')
	distinct_dates = _dates.distinct()
	#id for setup-checkbox
	ids = {}
	#id for packup-checkbox
	idp = {}
	l = 1
	#these are different ids used in the front end for checkbox feilds
	for key in distinct_dates:
		s = "button" + str(l)
		s1 = "but" + str(l)
		ids[key] = s
		idp[key] = s1
		l = l + 1

	if request.method=='POST':
		uid = request.session['the_id'] 
				
		if 'trail4' in request.POST:
			answer = request.POST.getlist('trail4',[])
			print('answer')
			print(answer)
			for i in answer:
				#handle for dates without '.' like march
				#tdate = 'Sept. 6, 2020'
				#dd = datetime.strptime(tdate,'%b %d, %Y')
				#print("DDDDDDDDDDDDDDDDDDD")
				#print(dd)
				dateformatcheck = 0
				#d = datetime.strptime(i,'%B. %d, %Y')
				try:
					datetime.strptime(i,'%b. %d, %Y')
				except ValueError:
					try:
						datetime.strptime(i,'%B %d, %Y')
						dateformatcheck = 1
					except ValueError:
						dateformatcheck = 2
					#dateformatcheck = 1
				if dateformatcheck==2:
					d = datetime.strptime(i.upper().replace("SEPT", "SEP"), "%b. %d, %Y")
				elif dateformatcheck==0:
					d = datetime.strptime(i,'%b. %d, %Y')
					
				else:
					d = datetime.strptime(i,'%B %d, %Y')
					
				user = User.objects.get(pk = uid)
				event = Event.objects.get(event_date=d)
				if(Availability.objects.filter(user_id=user,event_id=event,is_packup=False)).exists():
					continue
				else:
					if(Availability.objects.filter(user_id=user,event_id=event,is_packup=True)).exists():
						a = Availability.objects.get(user_id=user,event_id=event,is_packup=True)
						a.delete()
						a = Availability(user_id = user, event_id = event, is_packup = False)
						a.save()
					else:
						a = Availability(user_id = user, event_id = event, is_packup = False)
						a.save()

		if 'packup' in request.POST:
			answer = request.POST.getlist('packup',[])
			for i in answer:
				dateformatcheck = 0
				try:
					datetime.strptime(i,'%b. %d, %Y')
				except ValueError:
					dateformatcheck = 1
				if dateformatcheck==0:
					d = datetime.strptime(i,'%b. %d, %Y')
				else:
					d = datetime.strptime(i,'%B %d, %Y')
				user = User.objects.get(pk = uid)
				event = Event.objects.get(event_date=d)
				if(Availability.objects.filter(user_id=user,event_id=event,is_packup=True)).exists():
					continue
				else:
					if(Availability.objects.filter(user_id=user,event_id=event,is_packup=False)).exists():
						continue
					a = Availability(user_id = user, event_id = event, is_packup = True)
					a.save()

		
		return redirect('availability')
	
	else:
		dic_datespeople = {}
		setup_heads = {}  
		sound_heads = {}
		packuponly = {}
		event_names = {}
		for d in distinct_dates:
			event_ids = Event.objects.get(event_date = d[0])
			team = Availability.objects.filter(event_id=event_ids.pk,user_id__is_soundhead=False,user_id__is_setuphead=False,is_packup=False)
			setupheads = Availability.objects.filter(event_id=event_ids.pk,user_id__is_setuphead=True,is_packup=False)
			soundheads = Availability.objects.filter(event_id=event_ids.pk,user_id__is_soundhead=True,is_packup=False)
			packup = Availability.objects.filter(event_id=event_ids.pk,is_packup=True)
			dic_datespeople[d[0]] = team
			setup_heads[d[0]] = setupheads
			sound_heads[d[0]] = soundheads
			packuponly[d[0]] = packup
			event_names[d[0]] = event_ids

		print("NAMES")
		print(event_names)
		context = {
			'sound_heads' : sound_heads,
			'setup_heads' : setup_heads,
			'team' : dic_datespeople, 
			'packup' : packuponly,
			'dates' : distinct_dates,
			'event_names':event_names,
			'ids' : ids,
			'idp' : idp,
		}
		return render(request,'accounts/availability.html',context)

def createaccount(request):
	if request.method=='POST':
		email = request.POST['email']
		name = request.POST['name']
		phonenumber = request.POST['phonenumber']
		password = request.POST['password']
		if 'is_soundhead' in request.POST:
			is_soundhead = True
		else:
			is_soundhead = False

		if 'is_setuphead' in request.POST:
			is_setuphead = True
		else:
			is_setuphead = False
		if 'is_teamadmin' in request.POST:
			is_teamadmin = True
		else:
			is_teamadmin = False
		u = User.objects.create_user(name=name,email=email,phonenumber=phonenumber,is_soundhead=is_soundhead,is_setuphead=is_setuphead,is_teamadmin=is_teamadmin,is_active=True,password=password)
		u.save()
		messages.success(request, 'Successful!')
		return redirect('adminpage')
	else:

		return render(request,'accounts/createaccount.html')

def myroster(request):
	if(FinalRoster.objects.filter(user_id__email=request.user)).exists():
		
		myroster = FinalRoster.objects.filter(user_id__email=request.user)
		context = {
			'myroster' : myroster,
		}
		return render(request,'accounts/myroster.html',context)
	else:
		return redirect('availability')