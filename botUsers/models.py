#DJONGO
from djongo import models
from API.pk_model import ApiModel
from uuid import uuid4

class BotUser(ApiModel):
    def get_id():
        return BotUser.objects.all().count()

    # _id = models.ObjectIdField(db_column="_id", primary_key=True)
    chat_identifier = models.IntegerField(default=0)

    @staticmethod
    def get_bot_user(chat_id):
        try:
            return BotUser.objects.get(chat_identifier=chat_id)
        except BotUser.DoesNotExist:
            return None

    @staticmethod
    def create_bot_user(chat_id: int):
        ERR_EXIST = f"este chat ya ha sido registrado"
        ERR_CREATE = f"Hubo un error con el registro del usuario"

        if BotUser.get_bot_user(chat_id) is not None:
            return ERR_EXIST
        try:
            botuser = BotUser()
            botuser.chat_identifier = chat_id
            botuser.save()
        except Exception as e:
            return ERR_CREATE

    @staticmethod
    def delete_bot_user(chat_id):print(value)
        


    

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
    
    def get_permissions(chat_id: int):
        bot_user = BotUser.get_bot_user(chat_id)
        if bot_user is None:
            return None
        try:
            return BotUserPermissions.objects.get(user=bot_user)
        except BotUserPermissions.DoesNotExist:
            return None

    def create_permissions(chat_id):
        ERR_CREATE = "No se pudieron crear los permisos"
        permissions = BotUserPermissions.get_permissions(chat_id)
        if permissions is None:
            try:
                permissions = BotUserPermissions()
                permissions.save()
            except Exception as e:
                return ERR_CREATE

    def set_permissions(chat_id: int, id: bool=None, sub: bool=None, sup:bool=None):
        ERR_PERMISSIONS_NOT_EXISTS = "El usuario no tiene la configuración habilitada. Usa /settings enable"
        UPDATED_PERMISSIONS = "Permisos actualizados"
        try:
            permissions = BotUserPermissions.get_permissions()
            if permissions is None:
               return ERR_PERMISSIONS_NOT_EXISTS
            if id is not None:
                permissions.identity = id
            if sub is not None:
                permissions.subscriptions = sub
            if sup is not None:
                permissions.support_contact = sup
            permissions.save()
            return UPDATED_PERMISSIONS
        except Exception as e:
            return
        