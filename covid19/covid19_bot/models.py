from django.db import models
import json
#

class first_button(models.Model):
    buttons = models.CharField(max_length=50)

    def __str__(self):
        return self.buttons


class bot_user(models.Model):
    user_name= models.CharField(max_length=30, blank=True)
    user_id= models.IntegerField(blank=True)
    query =models.CharField(max_length=30, blank=True)
    country_notif = models.CharField(max_length=500, blank=True)
    date_country = models.CharField(max_length=50, blank=True)


class country_update(models.Model):
    name= models.CharField(max_length=30, blank=True)
    info= models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.name