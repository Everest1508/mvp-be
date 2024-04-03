from django.urls import path
from .views import EventParticipationAPIView,MyParticipationsAPIView
urlpatterns = [
    path('participate/',EventParticipationAPIView.as_view(),name="event-participate"),
    path('my-events/',MyParticipationsAPIView.as_view(),name="event-participate"),
]
