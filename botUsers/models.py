from djongo import models
from instances.models import Instance, Steps

class BotUser(models.Model):
    uid = models.IntegerField(default=0)

    class Meta:
        verbose_name = ("Bot User")
        verbose_name_plural = ("Bot Users")


class Subscription(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    chat = models.IntegerField()
    instance = models.ForeignKey(Instance, on_delete=models.DO_NOTHING)
    target_element = models.ForeignKey(Steps, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Suscripcion para {self.target_element} en {self.instance}'

    class Meta:
        verbose_name = ("Subscription")
        verbose_name_plural = ("Subscriptions")
