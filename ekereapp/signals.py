from django.db.models.signals import post_save
from .models import User
from django.db import models
from django.dispatch import receiver

@receiver(post_save,sender=User)
def Create_profile(sender,instance,created,**kwargs):
    if created:
        User.objects.create(user=instance)
        print('\n')
        print('profile created')
    
@receiver(post_save,sender=User)
def Update_profile(sender,instance,created,**kwargs):
    if created==False:
        instance.User.save()
        print('\n')
        print('profile updated')