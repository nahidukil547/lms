from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import (RegisterSerializer, LoginSerializer,CourseSerializer,ModuleSerializer,
                          LessonSerializer,RecodedVideoSerializer,EnrollmentSerializer,AssignmentSerializer,SubmissionSerializer )
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import UserProfile,Course,Module, Lesson, RecodedVideo, Enrollment, Assignment,Submission
from django.contrib.auth.models import User
from .permission import IsEmployee, PermissionMixin
# Create your views here.

# User = get_user_model()

class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = RegisterSerializer

class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = RegisterSerializer


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        try:
            user= User.objects.get(email = email)
        except User.DoesNotExist:
            return Response({'error':'Invalid Email Number'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_profile= UserProfile.objects.get(user=user)
            
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=status.HTTP_400_BAD_REQUEST)
        

        if not user.check_password(password):
            return Response({'error':'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)

        tokens = get_token_for_user(user)
        return Response({
            'messages':'Login Successfully',
            'tokens': tokens,
            "username":user.username,
            "email":user.email,
            "role":user_profile.role
        })

class LogOutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            refresh_token=request.data['refresh']
            token= RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully!"}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Token is invalid or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)


class CourseCreateListView(PermissionMixin, generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseUpdateDeleteView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class= CourseSerializer


class ModuleCreateListView(PermissionMixin, generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class=ModuleSerializer

    

class ModuleUpdateDeleteView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class= ModuleSerializer



class LessonCreateListView(PermissionMixin, generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class=LessonSerializer


class LessonUpdateDeleteView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class= LessonSerializer

class RecodedVideoListCreateView(PermissionMixin, generics.ListCreateAPIView):
    queryset = RecodedVideo.objects.all()
    serializer_class=RecodedVideoSerializer


class RecodedVideoUpdateDeleteView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = RecodedVideo.objects.all()
    serializer_class= RecodedVideoSerializer


class EnrollmentListCreateView(PermissionMixin, generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class=EnrollmentSerializer


class EnrollmentUpdateDeleteView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class= EnrollmentSerializer


class AssignmentListCreateView(PermissionMixin, generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class=AssignmentSerializer


class AssignmentUpdateDeleteView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class= AssignmentSerializer

class SubmissionListCreateView(PermissionMixin, generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class=AssignmentSerializer

class SubmissionUpdateDeleteView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class= SubmissionSerializer
