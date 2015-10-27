from django.contrib import admin
from dialogs.models import Message, Dialog

admin.site.register((Dialog, Message))
