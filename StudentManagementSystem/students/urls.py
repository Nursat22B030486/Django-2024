from django.urls import path
from .views import *
urlpatterns = [
    # path('', student_create_view, name='student_create'),
    path('', StudentListAPIView.as_view(), name='student_lists'),
    path('<int:pk>/', student_detail_view, name='student-detail'),
    path('<int:pk>/update/', student_update_view, name='student-update'),
    path('delete/<int:pk>/delete/', student_delete_view, name='student-delete'),
]