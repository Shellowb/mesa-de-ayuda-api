from django.contrib import admin
from .models import Subscription, SubscriptionOption
# Register your models here.

admin.site.register(Subscription)
admin.site.register(SubscriptionOption)
