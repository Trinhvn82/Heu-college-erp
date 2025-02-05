
from django.contrib.auth.models import User

user = User.objects.create_user(username='heu',
                                 email='',
                                 password='123654')

