from django.urls import path, re_path

from . import views

# name: id of url {% url 'index' %}
# Generic class-based detail view expects to be passed a parameter named pk
urlpatterns = [
    path("", views.index, name='index'),
    path("list/", views.ChatroomListView.as_view(), name='chat-list'),
    path("mine/", views.ChatroomOfUserListView.as_view(), name="my-chats"),
    path("mine/delete/<str:name>/", views.delete_mine_chatroom, name="delete-my-chat"),
    path("new/", views.create_chatroom, name='chat-create'),
    # re_path(r'^(?P<pk>\d+)/$', views.ChatroomDetailView.as_view(), name='chat-detail'),
    re_path(r'^chat/(?P<name>[\da-zA-Z_-]{3,})/$', views.show_chatroom, name='chat-detail-name'),
    re_path(r'^chat/(?P<name>[\da-zA-Z_-]{3,})/update/$', views.update_chatroom, name='chat-update'),
]
