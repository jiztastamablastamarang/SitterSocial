from .models import User, GENDERS
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.db import transaction
from .utils.hunter import email_status
from allauth.account import app_settings as allauth_settings
from django.utils.translation import gettext_lazy as _
from allauth.utils import email_address_exists
from .utils.clearbit import email_details


CUSTOM_FIELDS = (
                 "name",
                 "legal",
                 "founded",
                 "type",
                 "employees",
                 "description",
                 "parent_domain",
                 "ultimate_parent_domain",
                 "tags",
                 "industry",
                 "sector",
                 "sic_code",
                 "naics_code",
                 "technologies",
                 "technology_categories",
                 "alexa_global_rank",
                 "crunchbase",
                 "twitter",
                 "facebook",
                 "linkedin",
                 )


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
                     'pk',
                     'email',
                     'username',
                     'gender',
                 ) + CUSTOM_FIELDS
        read_only_fields = ('pk',)


class UserRegisterSerializer(RegisterSerializer):
    model = UserDetailsSerializer
    gender = serializers.ChoiceField(choices=GENDERS)

    def validate_email(self, email):
        email = self.initial_data.get('email')
        if email_status(email) != 'valid':
            raise serializers.ValidationError(_('Email does not exist.'), )
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(_('A user is already registered with this e-mail address.'), )
            else:
                return email

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.gender = self.data.get('gender')
        user.save()
        return user


class UserLoginSerializer(LoginSerializer):

    class Meta:
        model = User
        fields = ('email', 'password')
