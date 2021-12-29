from __future__ import print_function
from datetime import datetime, timedelta, time
import re
from djongo import models
from instances.models import Instance
import django.utils.timezone as tz
from django.utils.translation import gettext_lazy as _

class BotUser(models.Model):
    """Anonymous BotUser in the System
    This model is used to group user preferences
    and Functionalities"""
    id = models.ObjectIdField(db_column="_id", primary_key=True)
    uid = models.IntegerField(default=0)

    def get_create_bot_user(user):
        ERR_USER = '"Error al guardar el usuario"'
        try:
            new_user = BotUser.objects.get(uid=user)
        except Exception as e:
            try:
                new_user = BotUser(uid=user)
                new_user.save()
            except Exception as e1:
                return ERR_USER
    
    class Meta:
        verbose_name = ("Bot User")
        verbose_name_plural = ("Bot Users")


class SubscriptionLink(models.Model):
    """Is the link between the subscription
    and the Instance and Process elements.
    """
    class Destiny(models.IntegerChoices):
       TO_STEPS = 0, _('To Steps')
       TO_NEWS = 1, _('To News')
       TO_REQUISITES = 2, _('To Requisites')
       TO_FAQ = 3, _('To FAQ')
    #    __empty__ = None, _('To Nothing')

    instance = models.ForeignKey(Instance, on_delete=models.DO_NOTHING)
    # process = instance.process
    destiny = models.IntegerField(choices=Destiny.choices, blank=True)

    def __str__(self):
        return f'{self.destiny} en {self.instance}'
    
    class Meta:
        verbose_name = ('Subscription link')
        verbose_name_plural = ('Subscription links')

    @staticmethod
    def valid_link(target, frequency):
        valid_target = True if target in SubscriptionLink.Destiny.choices else False
        # valid_frequency = True if 

class Subscription(models.Model):
    """Holds the user subscription configuration.
    chat to send the responese
    the target element in the Process/Instance
    The frequency of the Notifications
    """
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    chat = models.IntegerField()
    target_element = models.ForeignKey(SubscriptionLink, on_delete=models.CASCADE)
    frequency = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Suscripcion para {self.target_element}'

    class Meta:
        verbose_name = ("Subscription")
        verbose_name_plural = ("Subscriptions")



class Notification(models.Model):
    """Saves the next message and next notification time for 
    a determined subscription"""
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    msg = models.TextField(max_length="500")
    next_notification = models.DateTimeField()

    def __str__(self):
        next = self.next_notification.strftime("%d-%m-%Y")
        holder = self.subscription.bot_user
        return f'Notification sch: {next} for: {holder}'

    def update_notification(self, msg="", next=None):
        """Set a new message and a new next notification date

        Args:
            msg (str, optional): [description]. Defaults to "".
            next ([type], optional): [description]. Defaults to None.
        """
        if next is None:
            next = self.next_notification + 1
        
        self.msg = msg
        self.next_notification = next

    # def get_steps_notification(freq=None):
    #     DEFAULT_WEEKS=2
    #     if freq is None:
    #         freq = timedelta(weeks=DEFAULT_WEEKS)
    #     msg = ""
        

    @staticmethod
    def get_today_notifications():
        today = tz.datetime.date(datetime.today())
        today_start = datetime.combine(today, time(hour=0, minute=0))
        today_end = datetime.combine(today, time(hour=23, minute=59))
        print(f'date:{today}')
        notifications = Notification.objects.filter(
            next_notification__range = (today_start, today_end)
        )
        return notifications

class BotUserPermissions(models.Model):
    """Bot User Permission set. Determines
    which functionalities are allowed by 
    the user.
    By default all are set to False.
    """
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    identity = models.BooleanField(default=False)
    subscriptions = models.BooleanField(default=False)
    support_contact = models.BooleanField(default=False)
        
        
    def __str__(self):
        id = 'Allowed' if self.identity else 'Not Allowed'
        sub = 'Allowed' if self.identity else 'Not Allowed'
        sup = 'Allowed' if self.identity else 'Not Allowed'
        return f'User:{self.user} id:{id} subscriptions:{sub} support contact:{sup}'

    @staticmethod
    def set_permissions(user_id, id=False, sub=False, sup=False):
        ERR_USER = 'This user appears to be inexisting'
        try:
            user = BotUser.objects.get(id=user_id)
            permissions = BotUserPermissions.objects.get(user=user)
        except Exception as e:
            return 'User:' + ERR_USER + f'\nid: Not Allowed \nsubscriptions: Not Allowed \nsupport contact: Not Allowed'
        permissions.identity = id
        permissions.subscriptions = sub
        permissions.support_contact = sup

        return f'Permissions set, {permissions}'