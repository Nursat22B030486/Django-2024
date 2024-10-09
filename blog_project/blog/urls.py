from django.contrib import admin
from django.urls import path
from .views import post_create, post_list, post_detail, post_edit, post_delete, AddCommentOnPostView

urlpatterns = [
    path('', post_list, name='post_list'),
    # path('search/', SearchResultsView.as_view(), name='search'), doesn't work as expected
    path('posts/<int:id>/', post_detail, name='post_detail'),
    path('posts/new/', post_create, name='post_create'),
    path('posts/<int:id>/edit/', post_edit, name='post_edit'),
    path('posts/<int:id>/delete/', post_delete, name='delete'),
    path('posts/<int:id>/comment/', AddCommentOnPostView.as_view(), name='add_comment'),
]