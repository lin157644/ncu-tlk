from django.urls import path, re_path
from . import views

# name: id of url {% url 'index' %}
# Generic class-based detail view expects to be passed a parameter named pk
urlpatterns = [
    path("", views.index, name='index'),
    path("list/", views.ChatroomListView.as_view(), name='chat-list'),
    path("mine/", views.ChatroomOfUserListView.as_view(), name="my-chats"),
    re_path(r'^(?P<pk>\d+)/$', views.ChatroomDetailView.as_view(), name='chat-detail'),
    path('login/', views.login, name='auth_login'),
    path('auth/', views.auth, name='auth'),
]
