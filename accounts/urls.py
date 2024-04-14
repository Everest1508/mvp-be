from django.urls import path
from .views import *
urlpatterns = [
    path("teacher-register/",TeacherRegisterAPIView.as_view(),name="teacher-register"),
    path("student-register/",StudentRegisterAPIView.as_view(),name="student-register"),
    path("login/",UserLoginAPIView.as_view(),name="login"),
    path("verify/",VerifyUserAPIView.as_view(),name="verify"),
    path('forget-password/', forget_password, name='forget-pass'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
]
