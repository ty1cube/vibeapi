from django.db import models
from datetime import datetime



class BaseModel(models.Model):

    long_description = models.CharField(
            max_length=70,
            null=True,
            blank=True,
            )

    created_on = models.DateTimeField(
            auto_now_add=True 
            )

    class Meta:
        abstract = True

    def __str__(self): 
        return str(self.id)



class MemberType(BaseModel):
    id = models.CharField(
            primary_key=True,
            max_length=1,
            unique=True
            )







