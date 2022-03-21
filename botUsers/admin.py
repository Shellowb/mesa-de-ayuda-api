from django.contrib import admin
from .models import BotUser, BotUserPermissions
# Register your models here.

admin.site.register(BotUser)
admin.site.register(BotUserPermissions)



