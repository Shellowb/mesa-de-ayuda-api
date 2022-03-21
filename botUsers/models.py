#DJONGO
from djongo import models
from API.pk_model import ApiModel
from uuid import uuid4

class BotUser(ApiModel):
    def get_id():
        return BotUser.objects.all().count()

    # _id = models.ObjectIdField(db_column="_id", primary_key=True)
    chat_identifier = models.IntegerField(default=0)


class BotUserPermissions(ApiModel):
    """Bot User Permission set. Determines
    which functionalities are allowed by 
    the user.
    By default all are set to False.
    """
    user = models.OneToOneField(to=BotUser, to_field="id", on_delete=models.CASCADE)
    identity = models.BooleanField(default=False)
    subscriptions = models.BooleanField(default=False)
    support_contact = models.BooleanField(default=False)
        