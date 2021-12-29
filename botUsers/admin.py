from django.contrib import admin
from .models import (
    BotUser,
    SubscriptionLink,
    Subscription,
    Notification,
    BotUserPermissions
)
# Register your models here.
admin.site.register(BotUser)
admin.site.register(SubscriptionLink)
admin.site.register(Subscription)
admin.site.register(Notification)
admin.site.register(BotUserPermissions)