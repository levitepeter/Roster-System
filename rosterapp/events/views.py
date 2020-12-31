from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.mail import send_mail
from django.conf import settings
#from django.core import mail
from django.db.models.functions import ExtractMonth
import calendar
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.html import strip_tags
from .models import Event,Availability,FinalRoster
from accounts.choices import month_choices
from datetime import date, datetime, timedelta
import os

def allevents(request):
	if request.method=='POST':
		month =int(request.POST['month'])
		current = datetime.now()
		d = date(current.year, month, 1)  
		d += timedelta(days = 6 - date.weekday(d))
		sundays=[]

		while d.month == month: # Loop only for current month
			sundays.append(d)  # Store Sunday dat
			d += timedelta(days = 7)  # Increment weekly (7 days)

		count = 1
		check = 0
		for i in sundays:
			event_name = i.strftime('%B') + '-Week-'
			event_name += str(count)
			count = count + 1
			event_date = i
			if(Event.objects.filter(event_date=event_date)).exists():
				check = 1
				break
				#do nothing
			else:
				e = Event(event_name=event_name,event_date=event_date)
				e.save()
		if check == 1:
			messages.error(request, 'Events for the selected month have already been created')
			return redirect('adminpage')
		to_mailid = list(User.objects.all())
		message = "Forms for " + calendar.month_name[int(month)] + " have been opened, please fill in your availability."
		subject = "Setup Forms Opened for " + calendar.month_name[int(month)]
		send_mail(
    	subject,
    	message,
    	'settings.EMAIL_HOST_USER',
    	to_mailid,
    	fail_silently=False,
		)

		messages.success(request, 'Events are created successfully!')
			#succes msg saying events created successfully
		return redirect('adminpage')
	else:
		context={
			'month_choices' : month_choices,
		}
	
		return render(request,'events/createallevents.html',context)


def viewroster(request):
	if request.method == 'GET':
		mon = request.GET.get("month",None)
		if mon:

			month = mon
			roster_for_month = FinalRoster.objects.filter(event_id__event_date__month=month)
			_dates = roster_for_month.values_list('event_id__event_date')
			distinct_dates = _dates.distinct()
			dic_datespeople = {}
			setup_heads = {}  
			sound_heads = {}
			packuponly = {}

			#month_name = datetime.date(2020, month, 1).strftime('%B')
			for d in distinct_dates:
				event_ids = Event.objects.get(event_date = d[0])
				team = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_soundhead=False,user_id__is_setuphead=False,is_packup=False)
				setupheads = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_setuphead=True,is_packup=False)
				soundheads = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_soundhead=True,is_packup=False)
				packup = FinalRoster.objects.filter(event_id=event_ids.pk,is_packup=True)
				dic_datespeople[d[0]] = team
				setup_heads[d[0]] = setupheads
				sound_heads[d[0]] = soundheads
				packuponly[d[0]] = packup

			context = {
				'month_name' : 'month_name',
				'mon' : mon,
				'sound_heads' : sound_heads,
				'setup_heads' : setup_heads,
				'team' : dic_datespeople, 
				'packup' : packuponly,
				'dates' : distinct_dates,
				'month_choices' : month_choices,
			
			}	

			return render(request,'events/viewroster.html',context)
		else:
			context={
			'month_choices' : month_choices,
			}
			return render(request,'events/viewroster.html',context)
	else:
		mon = request.POST['month']
		
		if mon:
			to_mailid = list(User.objects.all())
		 
			month = mon
			subject = "Setup Roster for " + calendar.month_name[int(month)]
			roster_for_month = FinalRoster.objects.filter(event_id__event_date__month=month)
			_dates = roster_for_month.values_list('event_id__event_date')
			distinct_dates = _dates.distinct()
			dic_datespeople = {}
			setup_heads = {}  
			sound_heads = {}
			packuponly = {}

			usr = FinalRoster.objects.filter(event_id__event_date__month=month)
			mail_ids = []
			for u in usr:
				_id = User.objects.filter(name=u)
				mail_ids.append(_id)
			#remove duplaicates from this and send mails to this later
				
			for d in distinct_dates:
				event_ids = Event.objects.get(event_date = d[0])
				team = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_soundhead=False,user_id__is_setuphead=False,is_packup=False)
				setupheads = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_setuphead=True,is_packup=False)
				soundheads = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_soundhead=True,is_packup=False)
				packup = FinalRoster.objects.filter(event_id=event_ids.pk,is_packup=True)
				dic_datespeople[d[0]] = team
				setup_heads[d[0]] = setupheads
				sound_heads[d[0]] = soundheads
				packuponly[d[0]] = packup

			context = {
				'month_name' : 'month_name',
				'sound_heads' : sound_heads,
				'setup_heads' : setup_heads,
				'team' : dic_datespeople, 
				'packup' : packuponly,
				'dates' : distinct_dates,
				'month_choices' : month_choices,
			
			}	


		#subject = 'HTML TEST MAIL'
		#here instead of viewroster.html create another html page wihtout the choose month button
		html_message = render_to_string('events/viewroster2.html', context)
		plain_message = strip_tags(html_message)
		send_mail(
    		subject,
    		plain_message,
    		'settings.EMAIL_HOST_USER',
    		to_mailid,
    		fail_silently=False,
    		html_message=html_message,
		)
		

		#from_email = 'From <from@example.com>'
		#to = 'to@example.com'

		#mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
		messages.success(request, 'Mails have been successfully sent!' )
		return redirect('viewroster')


def roster(request):
	if 'month' in request.POST:
    	
		month = request.POST['month']

		def sortByValue(dic):
			return sorted(dic.items(),key = lambda t:t[1])
		def updatetempdic(tempdic , track_roster_count):
			for key,value in tempdic.items():
				tempdic[key] = track_roster_count[key]
			return tempdic

		available_people = Availability.objects.all()

		#creates
		#find all the objects available for the 11th month
		available_for_month = Availability.objects.filter(event_id__event_date__month=month)
		#list only the dates
		_dates = available_for_month.values_list('event_id__event_date')
		#make note of the distinct dates which will be used later
		distinct_dates = _dates.distinct()

		#find the no of times people have given availability in a month ~ count and order by in sql
		frequency = available_for_month.values('user_id').annotate(freq=Count('user_id'))
		#sort the availabilities in asc
		freq_sorted = frequency.order_by('freq')
		dic_datespeople_packuponly={}
		 
		#dictionary that stores the dates and the list of people availible for that date
		dic_datespeople = {}
		#dict that stores who are rostreed in a month
		track_people_rostered = {}
		
		setup_heads = {}  
		sound_heads = {}
		track_roster_count = {}
		for d in distinct_dates:
			#find the event id of the current date for setup 
			event_ids = Event.objects.get(event_date = d[0])
			list_people_pack=[]
			if(Availability.objects.filter(event_id=event_ids.pk,is_packup=True)).exists():
				avail_forpackupoonly = Availability.objects.filter(event_id=event_ids.pk,is_packup=True)
				c = 0
				for i in avail_forpackupoonly:
					c=c+1
					list_people_pack.append(i)
					if c>=2:
						break
			else:
				print("Dont know what to write here<>")

			#create a list of people availble for every date
			list_people =[]
			maxcount = 0
			setup = 0
			sound = 0
			#temp is what stores the people who are availble for more than one day but have already been rostred iin a month once
			tempdic = {}
			
			for person in freq_sorted:
				usersid = person['user_id']
				#check if this user has given availility for this event
				if(Availability.objects.filter(event_id=event_ids.pk,user_id=usersid,is_packup=False).exists()):
					user = User.objects.get(id = usersid) 
					if(user.is_setuphead):
						if setup==0:
							setup = user.name
							track_people_rostered[user] = 'True'
							if user not in track_roster_count.keys():
								track_roster_count[user] = 1
									
							else:
								track_roster_count[user] = track_roster_count.get(user) + 1
							continue
					if(user.is_soundhead):
						if sound==0:
							sound = user.name
							track_people_rostered[user] = 'True'
							if user not in track_roster_count.keys():
								track_roster_count[user] = 1
							else:
								track_roster_count[user] = track_roster_count.get(user) + 1
							continue
					
					if maxcount<4:
							#save the person who is available for this event
							final_people = Availability.objects.get(event_id=event_ids.pk,user_id=usersid,is_packup=False)
							if user not in track_people_rostered:
								maxcount = maxcount + 1
								list_people.append(final_people)
								track_people_rostered[user] = 'True'
								if user not in track_roster_count.keys():
									track_roster_count[user] = 1
									
								else:
									track_roster_count[user] = track_roster_count.get(user) + 1
								
							else: 
								if user not in tempdic.keys():
									tempdic[user] = 1
									
								else:
									tempdic[user] = tempdic.get(user) + 1

			tempdic = updatetempdic(tempdic,track_roster_count)
			sorteddict = sortByValue(tempdic)
			#after iterating through all members, if more people are needed, then add 
			#others who were rostered previuosly and are available for the current event 
			if maxcount<4:
				for i in sorteddict:
					user = User.objects.get(email = i[0]) 
					temp_person = Availability.objects.get(event_id = event_ids.pk,user_id=i[0].id,is_packup=False)
					list_people.append(temp_person)
					track_roster_count[user] = track_roster_count.get(user) + 1
					maxcount = maxcount+1
					if maxcount>=4:
						break
			"""
			if maxcount<2:
				for i in temp:
					temp_person = Availability.objects.get(event_id=event_ids.pk,user_id=i.id)
					list_people.append(temp_person)
					if maxcount>=2:
						break
			"""
			dic_datespeople[d[0]] = list_people
			dic_datespeople_packuponly[d[0]] = list_people_pack
			setup_heads[d[0]] = setup
			sound_heads[d[0]] = sound
		
		for key,value in dic_datespeople.items():
				d = key
				event = Event.objects.get(event_date=d)
				if(FinalRoster.objects.filter(event_id__event_date=d,is_packup=False).exists()):
					messages.error(request, 'The roster has already been created!')
					#print an error message saying the roster has already been created
					#and click view to view roster
					return redirect("adminpage")
				else:
					for i in value:
						user =  User.objects.get(name =  i)
						a = FinalRoster(user_id = user, event_id = event, is_packup = False)
						a.save()
		messages.success(request, 'Roster is created successfully!')
					#print a success message saying the roster  is created
		
		for key,value in setup_heads.items():
			d=key
			event = Event.objects.get(event_date=d)
			if value!=0:
				user = User.objects.get(name=value)
				print("saving set")
				print(user)
				a = FinalRoster(user_id=user,event_id=event,is_packup=False)
				a.save()

		for key,value in sound_heads.items():
			d=key
			event = Event.objects.get(event_date=d)
			if value!=0:
				user = User.objects.get(name=value)
				print("saving sound")
				print(user)
				
				a = FinalRoster(user_id=user,event_id=event,is_packup=False)
				a.save()


		for key,value in dic_datespeople_packuponly.items():
			d = key
			event = Event.objects.get(event_date=d)
			if(FinalRoster.objects.filter(event_id__event_date=d,is_packup=True).exists()):
				#print an error message saying the roster has already been created
				messages.error(request, 'Roster for the selected month has already been created!')
				#and click view to view roster
				return redirect("adminpage")
			else:
				for i in value:
					user =  User.objects.get(name =  i)
					a = FinalRoster(user_id = user, event_id = event, is_packup = True)
					a.save()
				#print a success message saying the roster 
		
		print("sound head!")
		print(sound_heads);
		print("setup head!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print(setup_heads);
		context = {
			'sound_heads' : sound_heads,
			'setup_heads' : setup_heads,
			'dics' : dic_datespeople, 
			'packuponly' : dic_datespeople_packuponly,
			'available_people': available_people
		}
		return redirect('adminpage')
	else:
		#add a error message saying could not create 
		messages.error(request, 'It could not be created!')
		return redirect('adminpage')

def swap(request):
	if request.method == 'GET':
		date_from = request.GET.get("date_from",None)
		date_to = request.GET.get("date_to",None)
		if date_to:
			try:
				people_available = FinalRoster.objects.filter(event_id__event_date=date_to)
			except FinalRoster.DoesNotExist:
				#display error message
				messages.error(request, 'Please enter valid dates.')
				return redirect('swap')
			dic_people_available={}
			for p in people_available:
				dic_people_available[p] = p
			context={
			'date_from' : date_from,#use these as hidden values when sednig the post req
			'date_to' : date_to,
			'people_available' : people_available,
			'dic_people_available' : dic_people_available
			}
			return render(request,'events/swap.html',context)
		else:
			#if not working add empty conext
			return render(request,'events/swap.html')
	else:
		date_from = request.POST['from_date']
		date_to = request.POST['to_date']
		person_from = request.user.email
		if 'to_person' in request.POST:

			person_to = request.POST['to_person']
			try:
				val1 = FinalRoster.objects.filter(event_id__event_date=date_from)
			except FinalRoster.DoesNotExist:
				#error msg
				messages.error(request, 'You have not been rostered for the selected date!')
				return redirect('swap')
			try:
				val1 = val1.get(user_id__email=person_from)
			except FinalRoster.DoesNotExist:
				#error msg
				#check later
				#messages.error(request, 'The roster for this month has not been created yet, please try again after recieving the final roster mail!')
				messages.error(request, 'You have not been rostered for the selected date!')
				return redirect('swap')

			try:
				val2 = FinalRoster.objects.filter(event_id__event_date=date_to)
			except FinalRoster.DoesNotExist:
				#error msg
				messages.error(request, 'There are no rosters for the chosen dates!')
				return redirect('swap')

			try:
				val2 = val2.get(user_id__name=person_to)
			except FinalRoster.DoesNotExist:
				#error msg
				messages.error(request, 'Contact admin!')
				return redirect('swap')
			val1.delete()
			val2.delete()
			u1 = User.objects.get(email = person_from)
			e1 = Event.objects.get(event_date = date_from)
			u2 = User.objects.get(name = person_to)
			e2 = Event.objects.get(event_date = date_to)
			val1 = FinalRoster(event_id=e2,user_id = u1)
			val2 =FinalRoster(event_id=e1,user_id=u2)
			val1.save()
			val2.save()
			
			#Sedning MAils
			to_mailid = list(User.objects.all())
		 
			month = datetime.strptime(date_from, "%Y-%m-%d").month
			subject = "Setup Roster Updated for " + calendar.month_name[month] 
			roster_for_month = FinalRoster.objects.filter(event_id__event_date__month=month)
			_dates = roster_for_month.values_list('event_id__event_date')
			distinct_dates = _dates.distinct()
			dic_datespeople = {}
			setup_heads = {}  
			sound_heads = {}
			packuponly = {}

			usr = FinalRoster.objects.filter(event_id__event_date__month=month)
			mail_ids = []
			for u in usr:
				_id = User.objects.filter(name=u)
				mail_ids.append(_id)
			#remove duplaicates from this and send mails to this later
				
			for d in distinct_dates:
				event_ids = Event.objects.get(event_date = d[0])
				team = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_soundhead=False,user_id__is_setuphead=False,is_packup=False)
				setupheads = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_setuphead=True,is_packup=False)
				soundheads = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_soundhead=True,is_packup=False)
				packup = FinalRoster.objects.filter(event_id=event_ids.pk,is_packup=True)
				dic_datespeople[d[0]] = team
				setup_heads[d[0]] = setupheads
				sound_heads[d[0]] = soundheads
				packuponly[d[0]] = packup

			context = {
				'month_name' : 'month_name',
				'sound_heads' : sound_heads,
				'setup_heads' : setup_heads,
				'team' : dic_datespeople, 
				'packup' : packuponly,
				'dates' : distinct_dates,
				'month_choices' : month_choices,
			
			}	


			#subject = 'HTML TEST MAIL'
			#here instead of viewroster.html create another html page wihtout the choose month button
			html_message = render_to_string('events/viewroster2.html', context)
			plain_message = strip_tags(html_message)
			send_mail(
	    		subject,
	    		plain_message,
	    		'settings.EMAIL_HOST_USER',
	    		to_mailid,
	    		fail_silently=False,
	    		html_message=html_message,
			)
			
			messages.success(request, 'Swap was successfull!')
			return redirect('availability')
		else:
			#error msg
			messages.error(request, 'Please select a person from the list!')
			return redirect('swap')

def createextraevents(request):
	if request.method=='POST':
		event_name = request.POST['eventname']
		event_date = request.POST['eventdate']
		if(Event.objects.filter(event_date=event_date)).exists():
			messages.error(request, 'An Event for this date already exists')
			return redirect('adminpage')
		else:
			e = Event(event_name=event_name,event_date=event_date)
			e.save()
			#display success message
			messages.success(request, 'Event creation was a success!')
			return redirect('adminpage')
	else:
		return render(request,'events/createextraevents.html')


def currentteam(request):
	latest_month = FinalRoster.objects.latest('event_id').event_id.event_date.month

	month_name = calendar.month_name[latest_month]
	rosters = FinalRoster.objects.filter(event_id__event_date__month=latest_month)
	print(rosters)
	#rosters = FinalRoster.objects.filter(event_id__event_date__month=latest_month)
	roster_for_month = FinalRoster.objects.filter(event_id__event_date__month=latest_month)
	_dates = roster_for_month.values_list('event_id__event_date')
	distinct_dates = _dates.distinct()
	dic_datespeople = {}
	setup_heads = {}  
	sound_heads = {}
	packuponly = {}

	#remove duplaicates from this and send mails to this later
			
	for d in distinct_dates:
		event_ids = Event.objects.get(event_date = d[0])
		team = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_soundhead=False,user_id__is_setuphead=False,is_packup=False)
		setupheads = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_setuphead=True,is_packup=False)
		soundheads = FinalRoster.objects.filter(event_id=event_ids.pk,user_id__is_soundhead=True,is_packup=False)
		packup = FinalRoster.objects.filter(event_id=event_ids.pk,is_packup=True)
		dic_datespeople[d[0]] = team
		setup_heads[d[0]] = setupheads
		sound_heads[d[0]] = soundheads
		packuponly[d[0]] = packup
		context = {
				'month_name' : month_name,
				'sound_heads' : sound_heads,
				'setup_heads' : setup_heads,
				'team' : dic_datespeople, 
				'packup' : packuponly,
				'dates' : distinct_dates,
				'month_choices' : month_choices,
				'rosters' : rosters,
			}	


	return render(request,'events/currentteam.html',context)