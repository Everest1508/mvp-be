from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User, Teacher, Student
from .serializers import UserSerializer, TeacherSerializer, StudentSerializer
from django.shortcuts import render
from django.core.mail import send_mail
import random
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

class TeacherRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data['is_teacher'] = True
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = serializer.save(is_teacher=True)
            Teacher.objects.create(user=user)
            return Response({'msg': 'Teacher registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data['is_student'] = True
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = serializer.save(is_student=True)
            Student.objects.create(user=user)
            return Response({'msg': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyUserAPIView(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            otp = request.data['otp']
            user = User.objects.get(email=email, otp=otp)
            if user:
                user.is_trusty = True
                user.save()
                return Response({'msg': 'User verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            if not user.is_trusty:
                return Response({'msg': 'Profile is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
            token = get_tokens_for_user(user=user)
            data = {
                'token': token,
                'email': user.email,
                'is_teacher': user.is_teacher,
                'is_student': user.is_student
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class SendOTPView(APIView):
    def post(self,request):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                user.otp = random.randint(1000, 9999)
                user.save()

                subject = 'Forget Password OTP'
                message = f'Your OTP is: {user.otp}'
                from_email = settings.EMAIL_HOST_USER
                to_email = email
                send_mail(subject, message, from_email, [to_email])

                return Response({'detail': 'OTP sent successfully'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Email address is required'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if email and otp and new_password and confirm_password:
            # Validate OTP
            try:
                user = get_user_model().objects.get(email=email, otp=otp)
            except get_user_model().DoesNotExist:
                return Response({'error': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if new password and confirm password match
            if new_password != confirm_password:
                return Response({'error': 'New password and confirm password do not match'}, status=status.HTTP_400_BAD_REQUEST)

            # Change password
            user.set_password(new_password)
            user.save()

            user.otp = None
            user.save()

            return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)


def forget_password(request):
    print(request.POST)
    return render(template_name="forget_password.html",request=request)