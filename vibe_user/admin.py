from __future__ import absolute_import
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from vibe_user.forms import EmailUserCreationForm, EmailUserChangeForm
from vibe_user import models, const_models

class ConstantAdmin(admin.ModelAdmin):
    list_display = ('id',  'created_on')
    ordering = ('id',)

class SignupCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'ipaddr', 'created_on')
    ordering = ('-created_on',)
    readonly_fields = ('user', 'code', 'ipaddr')

    def has_add_permission(self, request):
        return False

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_on')
    ordering = ('-created_on',)

# class UserDefaultSpaceAdmin(admin.ModelAdmin):
#     list_display = ('user', 'space', 'created_on')
#     ordering = ('-created_on',)

class MemberAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'member_type', 'created_on')
    ordering = ('-created_on',)

class VibespotMemberAdmin(admin.ModelAdmin):
    list_display = ('user',  'is_member_admin', 'created_on')
    ordering = ('-created_on',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'created_on')
    ordering = ('-created_on',)


class SignupCodeInline(admin.TabularInline):
    model = models.SignupCode
    fieldsets = (
        (None, {
            'fields': ('code', 'ipaddr', 'created_on')
        }),
    )
    readonly_fields = ('code', 'ipaddr', 'created_on')

    def has_add_permission(self, request):
        return False


class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'created_on')
    ordering = ('-created_on',)
    readonly_fields = ('user', 'code')

    def has_add_permission(self, request):
        return False


class PasswordResetCodeInline(admin.TabularInline):
    model = models.PasswordResetCode
    fieldsets = (
        (None, {
            'fields': ('code', 'created_on')
        }),
    )
    readonly_fields = ('code', 'created_on')

    def has_add_permission(self, request):
        return False


class EmailUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password','is_verified',)}),
        # (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',"date_joined",)}),
    )
    readonly_fields=("date_joined",)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = EmailUserChangeForm
    add_form = EmailUserCreationForm
    inlines = [SignupCodeInline, PasswordResetCodeInline]
    list_display = ('email', 'is_verified', 
        'is_staff','username',)
    search_fields = ( 'email',)
    ordering = ('email',)


# admin.site.register(User, EmailUserAdmin)

admin.site.register(const_models.MemberType, ConstantAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.VibespotMember, VibespotMemberAdmin)
admin.site.register(models.SignupCode, SignupCodeAdmin)
admin.site.register(models.PasswordResetCode, PasswordResetCodeAdmin)

