from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User, Teacher, Student
from .serializers import UserSerializer, TeacherSerializer, StudentSerializer

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
            return Response({'message': 'Teacher registered successfully'}, status=status.HTTP_201_CREATED)
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
            return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyUserAPIView(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            otp = request.data['otp']
            user = User.objects.get(email=email,otp=otp)
            if user:
                user.is_trusty = True
                return Response()
            else:
                return Response()
        except:
            return Response()

class UserLoginAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            token = get_tokens_for_user(user=user)
            data = {
                'token': token,
                'email': user.email,
                'is_teacher': user.is_teacher,
                'is_student': user.is_student
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
