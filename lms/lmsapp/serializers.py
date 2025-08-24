from rest_framework import serializers
from .models import UserProfile,Course,Module,Lesson,RecodedVideo,Enrollment,Assignment, Submission
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User 


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def validate_username(self, value):
        user = self.instance 
        if User.objects.exclude(pk=user.pk if user else None).filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'phone', 'avatar', 'role',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        email = user_data.get('email')
        new_role = validated_data.get('role')
        try:
            exiting_user= User.objects.get(email=email)
            try:
                profile = UserProfile.objects.get(user = exiting_user)
                if profile.role == "Student" and new_role in ['Teacher','Employee']:
                    profile.role = new_role
                    profile.phone = validated_data.get('phone', profile.phone)
                    profile.avatar = validated_data.get('avatar', profile.avatar)
                    profile.is_active = validated_data.get('is_active', profile.is_active)
                    profile.save()
                    return profile
                else:
                    raise serializers.ValidationError({"email": f"This email is already registered with a different role.{profile.role}"}) 
            except:
                pass
        except: 
            user = UserSerializer().create(user_data)
            profile = UserProfile.objects.create(user=user, **validated_data)
            return profile
    
    def update(self, instance, validated_data):
        user_date= validated_data.pop('user')

        if user_date:
            UserSerializer().update(instance.user, user_date)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password=serializers.CharField(required=True)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Module
        fields='__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        fields='__all__'

class RecodedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=RecodedVideo
        fields='__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enrollment
        fields='__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Assignment
        fields='__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Submission
        fields='__all__'