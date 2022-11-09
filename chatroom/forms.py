from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Chatroom


class CreateChatForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    summary = forms.CharField(max_length=1000, required=True)
    is_public = forms.BooleanField(required=True)

    def clean_name(self):
        data = self.cleaned_data['name']
        if Chatroom.objects.filter(name__exact=data).exists():
            raise ValidationError(_('Chat name already exist'))
        return data

    def clean_summary(self):
        data = self.cleaned_data['summary']
        return data

    def clean_is_public(self):
        data = self.cleaned_data['is_public']
        return data
