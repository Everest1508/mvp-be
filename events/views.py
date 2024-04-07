from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import MainEvent, SubEvent,College
from .serializers import SubEventSerializer,MainEventSerializer,CollegeSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class SubEventCreateAPIView(generics.CreateAPIView):
    queryset = MainEvent.objects.all()
    serializer_class = SubEventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        main_event_id = kwargs.get('main_event_id')
        try:
            main_event = MainEvent.objects.get(pk=main_event_id)
        except MainEvent.DoesNotExist:
            return Response({'msg': 'Main event does not exist'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['main_event']=main_event.pk
        data['created_by']=request.user.pk
        data['college']=request.user.college
        print(request.user)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Subevent created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubEventListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,main_event):
        # try:
        main_event = MainEvent.objects.get(pk=main_event)
        events = SubEvent.objects.filter(main_event=main_event)
        serializer = SubEventSerializer(events, many=True)
        return Response(serializer.data)
        # except:
        #     return Response({'msg':'No Events Found'})
        
class MainEventListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            events = MainEvent.objects.all()
            serializer = MainEventSerializer(events, many=True)
            return Response(serializer.data)
        except:
            return Response({'msg':'No Events Found'})
        
class CollegeAPIView(generics.ListCreateAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    
class CreatedEventAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        events = SubEvent.objects.filter(created_by=request.user)
        return Response(SubEventSerializer(events,many=True).data)