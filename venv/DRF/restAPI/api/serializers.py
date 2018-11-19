from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from restAPI.tasks import new_user_length
from restAPI.models import UserModel, metadata
import logging
from restAPI.logConf import logf
logger = logf()

class UserSerializer(ModelSerializer):
    password_confirm = CharField(label='Confirm Password', style={'input_type':'password'})

    class Meta:
        model = UserModel
        fields =  [
            'username',
            'password',
            'password_confirm',
            'email',
        ]
        extra_kwargs = {'password': {'write_only': True}, 'password_confirm': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data['username'],validated_data['email'], validated_data['password'], validated_data['password_confirm'])
        user = UserModel(
                username = validated_data['username'],
                email = validated_data['email'],
               )
        if (validated_data['password'] == validated_data['password_confirm']):
            user.set_password(validated_data['password'])
            user.save()
            logger.info("New user created")
            new_user_length.delay()        #triggers the task
            return user
        else:
             logger.error ("Password mismatch!")
             raise ValidationError ("Password mismatch!")

class UpdatePasswordSerializer(ModelSerializer):
    old_password = CharField(required=True)
    password = CharField(label='new password', style={'input_type':'password'})
    confirm_password = CharField(label='confirm password', required=True, style={'input_type':'password'})

    class Meta:
        model = UserModel
        fields = [
            'old_password',
            'password',
            'confirm_password',
        ]

    def validate(self, data):
        validate_password(data['password'])
        return data

class LoginSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'username',
            'email',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

class APISerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'username',
            'active',
            'staff',
        ]