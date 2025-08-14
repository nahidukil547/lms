from django.urls import path
from .views import (UserProfileListCreateView, LoginView, UserProfileRetrieveUpdateView)

urlpatterns = [
    path('user/register/', UserProfileListCreateView.as_view(), name='register'),
    path('user/update/<int:pk>', UserProfileRetrieveUpdateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
] 