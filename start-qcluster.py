import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CollegeERP.settings")

import django
django.setup()

from django.core.management import call_command


from django_q.cluster import Cluster
import time

# Importing os module
import os
 
# Creating child processes using fork() method
os.fork()
os.fork()
 
# This will be executed by both parent & child processes

q = Cluster()

q.start()
time.sleep(60*10)  # Run for 10 minutes
q.stop()