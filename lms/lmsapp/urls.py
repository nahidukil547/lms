from django.urls import path
from .views import (UserProfileListCreateView, LoginView, UserProfileRetrieveUpdateView, LogOutView, CourseCreateListView,CourseUpdateDeleteView,
                    ModuleCreateListView,ModuleUpdateDeleteView)

urlpatterns = [
    path('user/register/', UserProfileListCreateView.as_view(), name='register'),
    path('user/update/<int:pk>/', UserProfileRetrieveUpdateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    
    # course API
    path('course/list/', CourseCreateListView.as_view(), name='course_list'),
    path('course/update/<int:pk>/', CourseUpdateDeleteView.as_view(), name='course_details'),

    path('module/list/', ModuleCreateListView.as_view(), name='course_list'),
    path('module/update/<int:pk>/', ModuleUpdateDeleteView.as_view(), name='course_details'),
    
] 