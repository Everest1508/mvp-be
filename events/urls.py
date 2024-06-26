from django.urls import path
from .views import SubEventCreateAPIView,SubEventListAPIView,MainEventListAPIView,CollegeAPIView,CreatedEventAPIView

urlpatterns = [
    path('main-event/<int:main_event_id>/create-subevent/', SubEventCreateAPIView.as_view(), name='create-subevent'),
    path('main-events/', MainEventListAPIView.as_view(), name='main-event-list'),
    path('main-event/<int:main_event>/sub-events/', SubEventListAPIView.as_view(), name='sub-event-list'),
    path('college/', CollegeAPIView.as_view(), name='college-list'),
    path('created-events/', CreatedEventAPIView.as_view(), name='created-event-list'),
]
