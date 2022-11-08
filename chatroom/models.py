from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Chatroom(models.Model):
    """Chatroom model"""

    # Fields
    name = models.CharField(
        max_length=255, help_text="Enter name of the chatroom"
    )
    summary = models.TextField(max_length=1000, help_text="Enter summary of the chatroom")
    user = models.ManyToManyField(User, related_name="chatroom_as_member")
    is_public = models.BooleanField(default=False, help_text="Choose whether the chatroom should be public")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chatroom_as_owner")
    created_at = models.DateTimeField(auto_now_add=True)

    # @property
    # def is_overdue(self):
    #     """Determines if the book is overdue based on due date and current date."""
    #     return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        """Meta definition for Chatroom."""
        ordering = ["-created_at", "name"]

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Chatroom."""
        return reverse("chat-detail", args=[str(self.id)])

    def __str__(self):
        """String for representing the Chatroom object (in Admin site etc.)."""
        # use str() for pylint
        return str(self.name)

    def display_users(self):
        """Create a string for the Users. This is required to display users in Admin."""
        return ', '.join(str(user.id) for user in self.user.all()[:3])

    display_users.short_description = 'Users'


class Message(models.Model):
    """Message model"""

    content = models.TextField(
        max_length=1000, help_text="Enter message content"
    )
    # If the chatroom is deleted the message will be deleted as well.
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.content)
