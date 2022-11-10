import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Chatroom


class CreateChatForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    # summary = forms.CharField(max_length=1000, required=False)
    # is_public = forms.BooleanField(required=False)

    # Use model form is possible
    # class Meta:
    #     model = Chatroom

    def clean_name(self):
        data = self.cleaned_data['name']
        if not re.fullmatch(r"[0-9A-Za-z_-]{3,}", data):
            raise ValidationError(_('Invalid chat name. Chat name must be of at least three character and only '
                                    'contain alphabet, number, "-" and "_"'))
        if Chatroom.objects.filter(name__exact=data).exists() or (data.isnumeric() and Chatroom.objects.filter(id__exact=int(data)).exists()):
            raise ValidationError(_('Chat name already exist'))
        return str(data)

    def clean_anonymous(self):
        data = self.cleaned_data['anonymous']
        if not isinstance(data, bool):
            raise ValidationError(_('Invalid anonymous input'))\

        return bool(data)


    # def clean_summary(self):
    #     data = self.cleaned_data['summary']
    #     return data
    #
    # def clean_is_public(self):
    #     data = self.cleaned_data['is_public']
    #     return data
