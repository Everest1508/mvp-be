from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
from events.models import SubEvent as Event
from .models import EventParticipant
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import EventParticipantSerializer

class EventParticipationAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        event_id = request.data.get('event_id')

        if user.is_teacher:
            return Response({'msg': 'Teachers cannot participate in events'}, status=status.HTTP_400_BAD_REQUEST)

        if not event_id:
            return Response({'msg': 'Event ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'msg': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        participant, created = EventParticipant.objects.get_or_create(user=user, event=event)
        if created:
            return Response({'msg': 'Participation successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'You are already participating in this event'}, status=status.HTTP_400_BAD_REQUEST)

class MyParticipationsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        participations = EventParticipant.objects.filter(user=user)
        serializer = EventParticipantSerializer(participations, many=True)
        return Response(serializer.data)
