from rest_framework import serializers
from events.models import SubEvent
from .models import EventParticipant
from accounts.serializers import UserSerializer
class SubEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubEvent
        fields = "__all__"
        

class EventParticipantSerializer(serializers.ModelSerializer):
    event = SubEventSerializer()
    user = UserSerializer()
    class Meta:
        model = EventParticipant
        fields = "__all__"