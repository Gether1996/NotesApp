from django.contrib.auth.models import User
from django.db.models import *


class CustomUser(User):
    address = CharField(max_length=100)
    city = CharField(max_length=100)
    zipcode = IntegerField()




