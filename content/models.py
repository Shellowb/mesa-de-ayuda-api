#DJONGO
from djongo import models
from API.pk_model import ApiModel
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import django.utils.timezone as tz
from instances.models import Instance
from botUsers.models import BotUser
from datetime import datetime, timedelta, time

class SubscriptionOption(ApiModel):
    """Is the link between the Instance and Process 
    elements (or content). It Allows the user to create
    a subscription. Also, the Instance-Content link list
    represents all available subscription options to the
    user.Inst
    """
    class Content(models.IntegerChoices):
       STEPS = 0, _('Etapas')
       NEWS = 1, _('Novedades')
       REQUISITES = 2, _('Requisitos')
       FAQ = 3, _('FAQ')
    #    __empty__ = None, _('To Nothing')

    class ContentType(models.IntegerChoices):
       DATES = 0, _('Fechas')   # dates related to some process for example steps or requisites
       INFO = 1, _('Información') # general info of some process actors or definitions
       UPDATES = 2, _('Novedades') # a change in the the process dates or info

    content = models.IntegerField(choices=Content.choices, blank=True)
    content_type = models.IntegerField(choices=ContentType.choices, blank=True)
    instance = models.ForeignKey(Instance, on_delete=models.DO_NOTHING)


    def __str__(self):
        return f'{self.label} en {self.instance}'
    
    class Meta:
        verbose_name = ('Subscription Option')
        verbose_name_plural = ('Subscription Options')

    @staticmethod
    def option_value(label):
        # label <-> FAQ.label -> FAQ (value)
        if label == SubscriptionOption.Content.FAQ.label:
            return SubscriptionOption.Content.FAQ
        # label <-> NEWS.label -> NEWS (value)
        if label == SubscriptionOption.Content.NEWS.label:
            return SubscriptionOption.Content.NEWS
        # label <-> STEPS.label -> STEPS (value)
        if label == SubscriptionOption.Content.STEPS.label:
            return SubscriptionOption.Content.NEWS
        # label <-> REQUISITES.label -> REQUISITES (value)
        if label == SubscriptionOption.Content.REQUISITES.label:
            return SubscriptionOption.Content.REQUISITES

    @property
    def label(self):
        # FAQ -> FAQ.label
        if self.Content == SubscriptionOption.Content.FAQ:
            return SubscriptionOption.Content.FAQ.label
        # NEWS -> NEWS.label
        if self.Content == SubscriptionOption.Content.NEWS:
            return SubscriptionOption.Content.NEWS.label
        # STEPS -> STEPS.label
        if self.Content == SubscriptionOption.Content.STEPS:
            return SubscriptionOption.Content.STEPS.label
        # REQUISITES -> REQUISITES.label
        if self.Content == SubscriptionOption.Content.REQUISITES:
            return SubscriptionOption.Content.REQUISITES.label

    @staticmethod
    def get_subscription_option(instance:Instance, Content: int):
        """A wrapper to django get with a generic Error Handling"""
        try:
            return SubscriptionOption.objects.get(instance=instance, Content=Content)
        except Exception as e:
            # DoesNotExist or multiple objects
            print(e)
            return None
    
    @staticmethod
    def aviable_options(instance: Instance=None, only_published=False) -> list[str]:
        if instance is not None:
            options = SubscriptionOption.objects.filter(instance=instance)
            if options.exists():
                return options
            return None

        if only_published:
            return SubscriptionOption.objects.select_related('instance').all()

        return SubscriptionOption.objects.all()

class Subscription(ApiModel):
    """Holds the user subscription configuration.
    chat to send the responese
    the target element in the Process/Instance
    The frequency of the Notifications
    """

    class Meta:
        verbose_name = ("Subscription")
        verbose_name_plural = ("Subscriptions")

    class SubscriptionType(models.IntegerChoices):
        EVENT = 0, _("Event") # notification when somthing happend
        DEADLINE = 1, _("Deadline") # notification as a remainder
        PERIODIC = 2, _("Periodic") # notification forever in a fixed rate
        # CONDITION = 3, _("Condition") # notification over a condition

    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    chat = models.IntegerField()
    target_content = models.ForeignKey(SubscriptionOption, on_delete=models.CASCADE)
    type = models.IntegerField(choices=SubscriptionType.choices)
    start = models.DateTimeField()
    end = models.DateTimeField()
    frequency = models.DurationField()
    created_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f'Suscripcion de {self.bot_user} para {self.target_content}'
    
    @property
    def description(self) -> str:
        return f'Suscripcion para {self.target_content}'

    @staticmethod
    def get_subscription(chat, target_content):
        try:
            return Subscription.objects.get(chat=chat, target_content=target_content)
        except Exception as e:
            return None

    @staticmethod
    def create_subscription(user: BotUser, chat: int, target: SubscriptionOption):
        """ ## create subscription

        recives a user, a chat_id and a target (instance link)
        and create a suscription to that user in that chat (for now the same),
        that respond to that target. the notifications are created to
        fixed frecuency in this version.

        Args:
            user (BotUser): BotUser object
            chat (int): chat identifier
            target (SubscriptionOption): suscription link between an instances and it's subscribable elements

        Returns:
            [str] : operation message.
        """
        ERR_SUBSCRIPTION = "Error en la creación de la subscripción"
        ERR_ALREADY_EXISTS = "La subscripción ya había sido creada"
        try:
            new_subscription = Subscription.get_subscription(chat,target)
            if new_subscription is not None:
                return ERR_ALREADY_EXISTS
            else:
                max_anticipation = timedelta(days=1, weeks=0)

                new_subscription = Subscription(
                    bot_user = user,
                    chat = chat,
                    target_content = target,
                    max_anticipation = max_anticipation
                )
                new_subscription.save()
                return "Subscripción Exitosa"
        except Exception as e:
            return ERR_SUBSCRIPTION

class Notification(ApiModel):
    """Saves the next message and next notification time for 
    a determined subscription"""
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    msg = models.TextField(max_length="500")
    next_notification = models.DateTimeField()

    def __str__(self):
        next = self.next_notification.strftime("%d-%m-%Y")
        holder = self.subscription.bot_user
        return f'Notification sch: {next} for: {holder}'


    def update_notification(self, msg=None, next=None):
        """Set a new message and a new next notification date

        Args:
            msg (str, optional): [description]. Defaults to "".
            next ([type], optional): [description]. Defaults to None.
        """
        if next is None:
            self.next_notification += self.subscription.frequency
        else:
            self.next_notification = next

        if msg is not None:
            self.msg = msg

    def calculate_next(self):
        try:
            subscription : Subscription = self.subscription
        except Exception as e:
            print(e)
            return None

        target : SubscriptionOption = subscription.target_content
        now = tz.now()
        type = subscription.type

        # FAQ -> n+1 = n+frequency
        if target.Content == SubscriptionOption.Content.FAQ:
            if self.next_notification is not None:
                self.next_notification += subscription.frequency
            else:
                self.next_notification = subscription.start + subscription.frequency     
        # NEWS -> NEWS.label
        if target.Content == SubscriptionOption.Content.NEWS:
            return SubscriptionOption.Content.NEWS.label
        # STEPS -> STEPS.label
        if target.Content == SubscriptionOption.Content.STEPS:
            return SubscriptionOption.Content.STEPS.label
        # REQUISITES -> REQUISITES.label
        if target.Content == SubscriptionOption.Content.REQUISITES:
            return SubscriptionOption.Content.REQUISITES.label

    @staticmethod
    def get_notifications(subscription: Subscription):
        try:
            return Notification.objects.filter(subscription=subscription)
        except Exception as e:
            return None
    
    # @staticmethod
    # def get_next_notification(subscription: Subscription, target):

    @staticmethod
    def create_notification(subscription: Subscription, msg: str, max_anticipation: timedelta):
        ERR_ALREADY_EXISTS = (-1, None)
        ERR_NOTIFICATION = (-2, None)
        try:    
            new_notification = Notification(
                subscription=subscription,
                msg=msg,
                max_anticipation=max_anticipation
            )
            new_notification.save()
            return (0, new_notification)
        except Exception as e:
            return ERR_NOTIFICATION

    

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
