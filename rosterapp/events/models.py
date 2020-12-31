from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
class Event(models.Model):
	event_name = models.CharField(max_length=40)
	event_date = models.DateField(auto_now=False,auto_now_add=False, unique=True)
	
	def __str__(self):
		return self.event_name
		

class Availability(models.Model):
	user_id = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
	event_id = models.ForeignKey(Event,on_delete=models.CASCADE)
	is_packup = models.BooleanField(default=False)


	def __str__(self):
		return self.user_id.name

class FinalRoster(models.Model):
	user_id = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
	event_id = models.ForeignKey(Event,on_delete=models.CASCADE)
	is_packup = models.BooleanField(default=False)


	def __str__(self):
		return self.user_id.name