from django.db.models.signals import post_save, post_delete
from . models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

def createProfile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(
            user = instance,
            username = instance.username,
            )

    subject = "Welcome"
    message = "We are glad you are here!"

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [instance.email],
        fail_silently=False,
    )


def deleteUser(sender, instance, *args, **kwargs):
    instance.user.delete()



post_save.connect(createProfile, sender=User)

post_delete.connect(deleteUser, sender=Profile)