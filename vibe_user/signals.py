from django.db.models.signals import post_save
from django.dispatch import receiver
from vibe_user import models
from .models import VibespotMember
from django.conf import settings 
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=models.User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    # Notice that we're checking for `created` here. We only want to do this
    # the first time the `User` instance is created. If the save that caused
    # this signal to be run was an update action, we know the user already
    # has a profile.
    if instance and created:
        instance.profile = models.Profile.objects.create(user=instance)


# @receiver(post_save, sender=models.Space)
# def create_space_assignment_space(sender, instance, created, *args, **kwargs):
#     if instance and created:
#         models.SpaceMember.objects.create(
#                 user=instance.creator, 
#                 space=instance,
#                 space_type=instance.space_type,
#                 is_space_admin=instance.is_space_admin,
#                 is_approved=True,
#             )

def set_vibespot_member(user, member, member_type, is_member_admin, is_approved):
    VibespotMember.objects.create(
                user=user, 
                member=member,
                member_type=member_type,
                is_member_admin=is_member_admin,
                is_approved=is_approved,
            )

# @receiver(post_save, sender=models.SpaceMember)
# def create_user_default_space(sender, instance, created, *args, **kwargs):
#     if instance and created:
#         models.UserDefaultSpace.objects.create(
#                 user=instance.user, 
#                 space=instance.space
#             )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
