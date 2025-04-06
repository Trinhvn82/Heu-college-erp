from django_q.models import Schedule
Schedule.objects.create(
    func='sms.tasks.fetch_tbs',  # module and func to run
#    minutes=60*24,  # run every 5 minutes
    minutes= 2 ,  # run every 2 minutes
    repeats=-1  # keep repeating, repeat forever
)