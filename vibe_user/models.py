import os
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
import jwt
from rest_framework.authtoken.models import Token
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django_countries import Countries
from django_countries.fields import CountryField
# from django.core.urlresolvers import reverse
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
# from dashboard.models import Organisation
from .const_models import MemberType
import uuid


# User = settings.AUTH_USER_MODEL

# class TimestampedModel(models.Model):

#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True
#         ordering = ['-created_on',"-updated_on"]




class UserManager(BaseUserManager):
    def create_user(self, username, email, member_type=None, password=None):
        if username is None:
            raise ValueError('Users must have a valid username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            member_type=member_type,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    username = models.CharField(db_index=True,max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    member_type        = models.ForeignKey(MemberType, on_delete=models.CASCADE, blank=True, null=True) 
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True,editable=True)
    updated_on = models.DateTimeField(auto_now=True,editable=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user'

    def create_user(self, username, email,  member_type=None, password=None):
        self.objects.create_user(
                username=username, 
                email=email,
                 member_type=member_type,
               
            )
        user.set_password(password)
        user.save()
        return user

    def __str__(self):
        """
        Returns a string representation of this `User`.

        """
        if self.username == None:
            return "User does not exist"
        return self.username

    def get_full_name(self):
        # The user is identified by their username
        if self.username == None:
            return "User does not exist"
        return self.username

    def get_short_name(self):
        # The user is identified by their username
        if self.username == None:
            return "User does not exist"
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Member(models.Model):
    # creator           = models.ForeignKey(User, on_delete=models.CASCADE)
    name              = models.CharField(primary_key=True, max_length=50, blank=False, null=False)
    member_type        = models.ForeignKey("vibe_user.MemberType", on_delete=models.CASCADE, blank=True, null=True) 
    is_active         = models.BooleanField(default=True)
    created_on        = models.DateTimeField(auto_now_add=True)
    updated_on        = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "member_type")

    def __str__(self):
        return self.name

class UserDefaultMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    member = models.ForeignKey(
            Member, 
            on_delete=models.CASCADE, 
        )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'userdefaultmember'

    def __str__(self):
        return self.user.username


class VibespotMember(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    space           = models.ForeignKey(Member,on_delete=models.CASCADE)
    member_type     = models.ForeignKey("vibe_user.MemberType", on_delete=models.CASCADE)
    is_member_admin  = models.BooleanField(default=False)
    is_approved     = models.BooleanField(default=False)
    approval_date   = models.DateTimeField(auto_now_add=True)
    created_on      = models.DateTimeField(auto_now_add=True)
    updated_on      = models.DateTimeField(auto_now=True)

    # class Meta:
    #     db_table = 'space_member'

    def __str__(self):
        return self.user.username



class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.user.username


def _generate_code():
    return uuid.uuid1(20)


class SignupCodeManager(models.Manager):
    def create_signup_code(self, user, ipaddr):
        code = _generate_code()
        if not ipaddr:
            ipaddr = "0.0.0.0"
        signup_code = self.create(user=user, code=code, ipaddr=ipaddr)

        return signup_code

    def set_user_is_verified(self, code):
        try:
            signup_code = SignupCode.objects.get(code=code)
            signup_code.user.is_verified = True
            signup_code.user.save()
            return True
        except SignupCode.DoesNotExist:
            pass
        return False


class PasswordResetCodeManager(models.Manager):
    def create_reset_code(self, user):
        code = _generate_code()
        password_reset_code = self.create(user=user, code=code)

        return password_reset_code


def send_multi_format_email(template_prefix, template_ctxt, target_email):
    subject_file = 'vibespot/%s_subject.txt' % template_prefix
    txt_file = 'vibespot/%s.txt' % template_prefix
    html_file = 'vibespot/%s.html' % template_prefix

    subject = render_to_string(subject_file).strip()
    from_email = settings.DEFAULT_EMAIL_FROM
    to = target_email
    # bcc_email = settings.DEFAULT_EMAIL_BCC
    text_content = render_to_string(txt_file, template_ctxt)
    html_content = render_to_string(html_file, template_ctxt)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


class AbstractBaseCode(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    code = models.CharField(_('code'), max_length=60, default="")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def send_email(self, prefix):
        ctxt = {
            'email': self.user.email,
            # 'first_name': self.user.first_name,
            # 'last_name': self.user.last_name,
            'code': self.code
        }
        send_multi_format_email(prefix, ctxt, target_email=self.user.email)

    def __str__(self):
        return self.code


class SignupCode(AbstractBaseCode):
    ipaddr = models.GenericIPAddressField(_('ip address'),default='0.0.0.0')
    objects = SignupCodeManager()

    class Meta:
        db_table = 'signupcode'
    
    def send_signup_email(self):
        prefix = 'signup_email'
        self.send_email(prefix)


class PasswordResetCode(AbstractBaseCode):
    objects = PasswordResetCodeManager()

    class Meta:
        db_table = 'passwordresetcode'

    def send_password_reset_email(self):
        prefix = 'password_reset_email'
        self.send_email(prefix)



