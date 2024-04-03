from rest_framework import serializers
from .models import SubEvent,MainEvent
from participants.models import EventParticipant
from participants.serializers import EventParticipantSerializer

class SubEventSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    class Meta:
        model = SubEvent
        fields = ['title', 'game', 'description', 'rules','main_event','participants']
        
    def get_participants(self,obj):
        participants = EventParticipant.objects.filter(event=obj)
        return EventParticipantSerializer(participants,many=True).data

class MainEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainEvent
        fields = "__all__"
