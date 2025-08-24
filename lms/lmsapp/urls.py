from django.urls import path
from .views import (UserProfileListCreateView, LoginView, UserProfileRetrieveUpdateView, LogOutView, CourseCreateListView,CourseUpdateDeleteView,
                    ModuleCreateListView,ModuleUpdateDeleteView,LessonCreateListView,LessonUpdateDeleteView
                    ,AssignmentListCreateView,AssignmentUpdateDeleteView,SubmissionListCreateView,SubmissionUpdateDeleteView,
                    RecodedVideoListCreateView,RecodedVideoUpdateDeleteView,EnrollmentListCreateView,EnrollmentUpdateDeleteView)

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
    
    path('lesson/list/', LessonCreateListView.as_view(), name='course_list'),
    path('lesson/update/<int:pk>/', LessonUpdateDeleteView.as_view(), name='course_details'),
    
    path('video/list/', RecodedVideoListCreateView.as_view(), name='course_list'),
    path('video/update/<int:pk>/', RecodedVideoUpdateDeleteView.as_view(), name='course_details'),
    
    path('enrollment/list/', EnrollmentListCreateView.as_view(), name='course_list'),
    path('enrollment/update/<int:pk>/', EnrollmentUpdateDeleteView.as_view(), name='course_details'),
    
    path('assignment/list/', AssignmentListCreateView.as_view(), name='course_list'),
    path('assignment/update/<int:pk>/', AssignmentUpdateDeleteView.as_view(), name='course_details'),
    
    path('assignment/list/', SubmissionListCreateView.as_view(), name='course_list'),
    path('assignment/update/<int:pk>/', SubmissionUpdateDeleteView.as_view(), name='course_details'),
] 