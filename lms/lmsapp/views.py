from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from django.contrib.auth.models import User

# Create your views here.

# User = get_user_model()

class UserProfileListCreateView(generics.ListCreateAPIView):
    print('in register view')
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
        except user.DoesNotExist:
            return Response({'error':'Invalid Email Number'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_profile= UserProfile.objects.get(user=user)
            
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=status.HTTP_400_BAD_REQUEST)
        

        if not user.check_password(password):
            return Response({'error':'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)

        tokens = get_token_for_user(user)

        profile_data = {
            "id": user_profile.id,
            "User": {
                "username":user.username,
                "email":user.email,
                "First Name":user.first_name,
                "Last Name":user.last_name,
            },
            "phone": user_profile.phone,
            "avatar": user_profile.avatar,
            "role": user_profile.role,
            "is_active": user_profile.is_active,
            "created_at": user_profile.created_at,
            "updated_at": user_profile.updated_at
        }
        return Response({
            'messages':'Login Successfully',
            # 'user_id':user.id,
            # 'username':user.username,
            'tokens': tokens,
            'user_details':profile_data
        })







