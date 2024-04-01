from rest_framework import serializers
from .models import User, Teacher, Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'phone', 'age', 'college', 'is_active', 'is_staff', 'is_teacher', 'is_student', 'otp')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            name=validated_data.get('name', ''),
            phone=validated_data.get('phone', ''),
            age=validated_data.get('age', ''),
            college=validated_data.get('college', ''),
            is_active=validated_data.get('is_active', True),
            is_staff=validated_data.get('is_staff', False),
            is_teacher=validated_data.get('is_teacher', False),
            is_student=validated_data.get('is_student', False),
            otp=validated_data.get('otp', None)
        )
        return user

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Embedding UserSerializer

    class Meta:
        model = Teacher
        fields = ('user',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance = User.objects.create(**user_data)
        teacher = Teacher.objects.create(user=user_instance, **validated_data)
        return teacher

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Embedding UserSerializer

    class Meta:
        model = Student
        fields = ('user',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance = User.objects.create(**user_data)
        student = Student.objects.create(user=user_instance, **validated_data)
        return student
