from django.contrib import admin
from .models import Recipient, Message

admin.site.register(Recipient)
admin.site.register(Message)
