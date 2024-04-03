from django.urls import path
from .views import *
urlpatterns = [
    path("teacher-register/",TeacherRegisterAPIView.as_view(),name="teacher-register"),
    path("student-register/",StudentRegisterAPIView.as_view(),name="student-register"),
    path("login/",UserLoginAPIView.as_view(),name="login"),
    path("verify/",VerifyUserAPIView.as_view(),name="verify"),
]
