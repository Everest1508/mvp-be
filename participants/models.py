from django.db import models
from django.conf import settings
from events.models import SubEvent as Event
from django.utils import timezone

# Create your models here.
class EventParticipant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participation_time = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user.email} - {self.event.title}'