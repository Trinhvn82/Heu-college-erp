
import os; 
import django;

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CollegeERP.settings")
django.setup()

from django.contrib.sites.models import Site

my_site = Site(domain='127.0.0.1:8000', name='127.0.0.1:8000')

my_site.save()
print(my_site.id)