from django.urls import path
from .views import SubEventCreateAPIView,SubEventListAPIView,MainEventListAPIView

urlpatterns = [
    path('main-event/<int:main_event_id>/create-subevent/', SubEventCreateAPIView.as_view(), name='create-subevent'),
    path('main-events/', MainEventListAPIView.as_view(), name='main-event-list'),
    path('main-event/<int:main_event>/sub-events/', SubEventListAPIView.as_view(), name='sub-event-list'),
]
