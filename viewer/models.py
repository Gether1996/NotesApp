from django.contrib.auth.models import User
from django.db.models import *


class Category(Model):
    name = CharField(max_length=50)

    def __str__(self):
        return self.name


class Note(Model):
    COLD = 'Cold'
    MODERATE = 'Moderate'
    WARM = 'Warm'
    WEATHER_CHOICES = [
        (COLD, 'Cold (below 0°C)'),
        (MODERATE, 'Moderate (0-15°C)'),
        (WARM, 'Warm (16°C +)'),
    ]
    user = ForeignKey(User, on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=CASCADE)
    name = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    scheduled_time = DateTimeField(blank=True, null=True)
    description = TextField()
    preferred_weather = CharField(max_length=50, choices=WEATHER_CHOICES, blank=True)
    finished = BooleanField(default=False)

    def __str__(self):
        return f"({self.user.username}) {self.name} (Done)" if self.finished == True else f"({self.user.username}) {self.name} (In progress)"
