from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated
from django.db.models.signals import post_save

# Create your models here.

class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20,default="not-assign",choices=[('admin','admin'),('TA','TA'),("not-assign","not-assign")])

    def __str__(self):
        return self.role

class UnivChoices(models.Model):
    nama = models.CharField(max_length=30)

    def __str__(self):
        return self.nama

class Univ(models.Model):
    univ = models.ForeignKey(UnivChoices,on_delete=models.CASCADE,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_role(instance, created, **kwargs):
    """Create user profile if user object was just created."""
    if created:
        
        Role.objects.create(user=instance)


@receiver(cas_user_authenticated)
def save_user_attributes(user, attributes, **kwargs):
    user.save()
    user.email = f'{user.username}@ui.ac.id'
    full_name = attributes['nama']
    i = full_name.rfind(' ')
    user.first_name, user.last_name = full_name[:i], full_name[i + 1:]
    