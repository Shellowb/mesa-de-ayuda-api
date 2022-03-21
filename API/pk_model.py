# ------------> DISCLAIMER !!
# This module was created beacuse djongo an django doesn't autogerate the id for new objects always
# there strange almost arbitray situations in which id is generated and other that dont.
# to avoid recreate al sintaxis, this Super model is created in order to generate de id only

from djongo import models
from uuid import uuid4

class ApiModel(models.Model):
    class Meta: abstract = True

    id = models.CharField(
        max_length=36, 
        unique=True, 
        primary_key=True,
        default = uuid4,
        editable = False)