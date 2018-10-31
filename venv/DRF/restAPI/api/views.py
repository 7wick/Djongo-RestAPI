from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError
from django.forms.models import model_to_dict
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)
from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
)
from .serializers import (
    UserSerializer,
    LoginSerializer,
    UpdatePasswordSerializer
)
from restAPI.models import UserModel
import logging
from restAPI.logConf import logf
logger = logf()

class UserAuthAPIView(ModelViewSet):
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_object(self, queryset=None):
        return self.request.user

    @action(methods=['post'],detail=False, permission_classes=[IsAuthenticated], serializer_class=UpdatePasswordSerializer)
    def updatepass(self, request, *args, **kwargs):
        data = request.data
        self.object = self.get_object()
        serializer = UpdatePasswordSerializer(data=data, many=True)
        if serializer.is_valid():
            old_password = data['old_password']
            if not self.object.check_password(old_password):
                logger.error("Wrong password")
                return Response("Wrong password!", status=HTTP_400_BAD_REQUEST)
            if (data['password'] == data['confirm_password']):
                if (data['password'] == data['old_password']):
                    logger.error("Password cannot be the same as used earlier")
                    raise ValidationError ("Password cannot be the same as used earlier!")
                else:
                    self.object.set_password(data['password'])
                    self.object.save()
                    logger.info("Password changed for {}".format(self.object.username))
                    return Response("Password changed successfully!", status=HTTP_200_OK)
            else:
                logger.error ("Password mismatch!")
                raise ValidationError ("Password mismatch!")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action (methods=['post'], detail=False, serializer_class=LoginSerializer, permission_classes=[AllowAny])
    def login(self, request, *args, **kwargs):
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']
        if not all((username, email, password)):
            logger.error("Credentials missing!")
            raise ValidationError ("Credentials missing!")
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            logger.error ("Such user does not exists")
            raise ValidationError('Such user does not exists')
        if (user.username != username):
            logger.error ("Credentials incorrect!")
            raise ValidationError("Credentials incorrect!")
        if not user.check_password(password):
            logger.error ("Password incorrect!")
            return Response ("Password incorrect!", status=HTTP_400_BAD_REQUEST)
        login (self.request, user)  #logs-in the user
        logger.info ("{} has logged-in".format(user.username))
        return Response (model_to_dict(user, exclude = ['password','groups',]), status=HTTP_200_OK) #returning data from DB

    @action (methods=['destroy'], detail=False, permission_classes=[IsAuthenticated])
    def delete(self, request, *args, **kwargs):
        user = self.get_object ()
        user.delete ()
        logger.info ("{}`s account has been deleted".format (user.username))
        return Response ('User deleted')