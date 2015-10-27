# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from bubble.forms import BootstrapFormMixin
from dialogs.models import Message


class MessageForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Message
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'rows': 4, 'placeholder': _(u'напишіть повідомлення')})}

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def clean_text(self):
        return self.cleaned_data['text'].strip()