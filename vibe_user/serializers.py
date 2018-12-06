from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
# from django_countries.serializer_fields import CountryField
# from django_countries.data import COUNTRIES

from .models import (
        Member,
        User,
        Profile,
        UserDefaultMember,
        VibespotMember,
)

# from dashboard.models import (
#         Organisation
#     )

# from .const_models import (
#         Country,
#         )


class BaseSignupSerializer():
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )


    def create(self, validated_data):
        user = User.objects.create_user(
                validated_data['username'], 
                validated_data['email'],
                validated_data['password']
                )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(required=True,min_length=8)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model  = User 
        # fields = ("id", "username", "email", "password", "token")
        fields = "__all__"
        read_only_field = ("created_on", "updated_on")

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)




class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Member
        fields = "__all__"
        read_only_field = ("created_on", "updated_on")


class UserDefaultMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserDefaultMember 
        fields = "__all__"
        read_only_fields = ("created_on", "updated_on")



class ArtistMemberSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()
    class Meta:
        model  = VibespotMember 
        fields = "__all__"
        read_only_field = ("created_on", "updated_on")

    def get_member(self, obj):
        return {
            "member_id": obj.member.id,
            "member_name": obj.member.name,
        }


class RecordMemberSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()
    class Meta:
        model  = VibespotMember 
        fields = "__all__"
        read_only_field = ("created_on", "updated_on")

    def get_member(self, obj):
        return {
            "member_name": obj.member.name,
        }



class VibespotMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model  = VibespotMember
        fields = "__all__"
        read_only_field = ("created_on", "updated_on")



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User 
        fields = ("id", "username", "email")


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer();

    class Meta:
        model  = Profile
        fields = "__all__"
        # fields = ("id", "username", "email")
        read_only_fields = ("created_on", "updated_on")


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class PasswordResetVerifiedSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128)


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)







