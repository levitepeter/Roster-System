"""
from django_cron import cronScheduler, Job
import sys

class Test(Job):
    print("class ran")
    run_every=60
    def job(self):
        print("job ran")

cronScheduler.register(Test)

from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 1 min

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'emails.cron'    # a unique code

    def do(self):
    	print("class ran")
   """
 def my_cron_job():
    # your functionality goes here
    print("RUNNING CRON FOR MAIL")