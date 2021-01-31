from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  cargo = models.ForeignKey('Cargo', on_delete=models.PROTECT)

  def __str__(self):
    return self.user.get_full_name()


class Cargo(models.Model):
  name = models.CharField(max_length=70, blank=False, default='')
  description = models.TextField(blank=False, default='')

  def __str__(self):
    return self.name