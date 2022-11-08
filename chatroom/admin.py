from django.contrib import admin
from .models import Chatroom, Message

class MessagesInstanceInline(admin.TabularInline):
    model = Message

# admin.site.register(Chatroom)
@admin.register(Chatroom)
class ChatroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'display_users')
    # list_filter = ('status', 'due_back')
    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'created_at', 'id')
    #     }),
    #     ('Something else', {
    #         'fields': ('status', 'due_back')
    #     }),
    # )
    inlines = [MessagesInstanceInline]


# admin.site.register(Message)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at')
