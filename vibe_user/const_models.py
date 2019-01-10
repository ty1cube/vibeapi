from django.db import models
from datetime import datetime



class BaseModel(models.Model):

    name = models.CharField(
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
            max_length=3,
            unique=True
            )


class Country(BaseModel):
    id = models.CharField(
            primary_key=True,
            max_length=3,
            unique=True
        )
 
    class Meta:
        db_table = 'country'



class State(BaseModel):
    id = models.CharField(
            primary_key=True,
            max_length=4,
            unique=True
        )

    country_id =  models.CharField(
            max_length=3,
            null=True,
            blank=True,
        )
 
    class Meta:
        db_table = 'state'


class LocalArea(BaseModel):
    id = models.CharField(
            primary_key=True,
            max_length=3,
            unique=True
        )

    state_id =  models.CharField(
            max_length=4,
            null=True,
            blank=True,
        )
 
    class Meta:
        db_table = 'localarea'





