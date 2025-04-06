from django.shortcuts import render, get_object_or_404, redirect
from notifications.signals import notify
from django_q.models import Schedule
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User


User = get_user_model()

def fetch_tbs():

    print("fetch_tbs is running...")

    user = User.objects.get(username='heu-demo')

    notify.send(sender=user, recipient=user, verb='you loaded the page tested by schedule', level='success')

#    pass  # do whatever logic you want here

def schedule_fetch_tbs(request):
    #pass
    a = Schedule.objects.create(
        func='sms.tasks.fetch_tbs',  # module and func to run
    #    minutes=60*24,  # run every 5 minutes
        minutes= 2 ,  # run every 2 minutes
        repeats=-1  # keep repeating, repeat forever
    )
    return redirect("lop_list")