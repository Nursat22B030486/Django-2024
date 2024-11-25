from django.urls import path
from .views import *

urlpatterns = [
    path('', CourseCreateAPIView.as_view(), name='course-create'),
    path('list/', CourseListAPIView.as_view(), name='course-list'),
    path('<int:pk>/update/', CourseUpdateAPIView.as_view(), name='course-update'),
    path('<int:pk>/delete/', CourseDeleteAPIView.as_view(), name='course-delete'),
    path('<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('enrollment/', EnrollmentListCreateAPIView.as_view(), name='enrollment-create'),
    path('enrollment/<int:pk>/', EnrollmentDetailAPIView.as_view(), name='enrollment-detail'),
    path('enrollment/<int:pk>/delete/', EnrollmentDeleteAPIView.as_view(), name='enrollment-delete'),
]