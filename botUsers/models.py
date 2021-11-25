from django.db import models
from django.db.models.lookups import In
from instances.models import Instance, Steps

class BotUser(models.Model):
    uid = models.IntegerField()

    class Meta:
        verbose_name = ("Bot User")
        verbose_name_plural = ("Bot Users")


class Subscription(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    instance = models.ForeignKey(Instance, on_delete=models.DO_NOTHING)
    target_element = models.ForeignKey(Steps, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = ("Subscription")
        verbose_name_plural = ("Subscriptions")
