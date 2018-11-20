from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from django.contrib.auth import login, logout
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
    IsAdminUser,
)
from .serializers import (
    UserSerializer,
    LoginSerializer,
    UpdatePasswordSerializer,
    APISerializer,
)
from restAPI.models import UserModel
from restAPI.logConf import logf
logger = logf()

class UserAuthAPIView(ModelViewSet):
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_object(self, queryset=None):
         return self.request.user
        # if queryset is None:
        #     queryset = self.get_queryset ()
        #
        #     # Next, try looking up by primary key.
        # # pk = self.kwargs.get (self.id)
        # if id is not None:
        #     queryset = queryset.filter (id=id)
        #
        # # If none of those are defined, it's an error.
        # if id is None:
        #     raise AttributeError (
        #         "Generic detail view %s must be called with either an object "
        #         "pk or a slug in the URLconf." % self.__class__.__name__
        #     )
        #
        # try:
        #     # Get the single item from the filtered queryset
        #     obj = queryset.get ()
        # except queryset.model.DoesNotExist:
        #     raise ValidationError("No %(verbose_name)s found matching the query")
        # return obj

    @action (methods=['post'], detail=False, serializer_class=UserSerializer, permission_classes=[AllowAny])
    def createuser(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response("user created successfully", status=HTTP_200_OK)
        return Response("failed",status=HTTP_400_BAD_REQUEST)

    @action (methods=['post'], detail=False, serializer_class=LoginSerializer, permission_classes=[AllowAny])
    def login(self, request, *args, **kwargs):

        # print(request.user.is_authenticated)
        #
        # if request.user.is_authenticated:
        #     return Response("Someone is already logged-in", status=HTTP_400_BAD_REQUEST)
        #     #logout (self.request)
        # else:
            data = request.data
            username = data['username']
            email = data['email']
            password = data['password']
            if not all ((username, email, password)):
                logger.error ("Credentials missing!")
                raise ValidationError ("Credentials missing!")
            try:
                user = UserModel.objects.get (email=email)
            except UserModel.DoesNotExist:
                logger.error ("Such user does not exists")
                raise ValidationError ('Such user does not exists')
            if (user.username != username):
                logger.error ("Credentials incorrect!")
                raise ValidationError ("Credentials incorrect!")
            if not user.check_password (password):
                logger.error ("Password incorrect!")
                return Response ("Password incorrect!", status=HTTP_400_BAD_REQUEST)
            login (self.request, user)  # logs-in the user
            logger.info ("{} has logged-in".format (user.username))
            return Response ("Login success", status=HTTP_200_OK)
        # return Response (model_to_dict(user, exclude = ['password','groups',]), status=HTTP_200_OK) #returning data from DB

    @action (methods=['post', 'get'], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        logout(self.request)
        return Response ("User logged-out successfully", status=HTTP_200_OK)

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

    @action (methods=['destroy'], detail=False, permission_classes=[IsAuthenticated])
    def delete(self, request, *args, **kwargs):
        user = self.request
        user.delete ()
        logout (user)
        logger.info ("{}`s account has been deleted".format (user.username))
        return Response ('User deleted')

    @action (methods=['put'], detail=False, serializer_class=APISerializer, permission_classes=[IsAdminUser])
    def active(self, request):
        data = request.data
        try:
            user = UserModel.objects.get(username = data['username'])
            if user is not None:
                try:
                    if data.get('active'):
                        user.active = True
                except MultiValueDictKeyError:   # or use data.get('active')
                    user.active = False
                try:
                    if data.get('staff'):
                        user.staff = True
                except MultiValueDictKeyError:
                    user.staff = False
                user.save()
        except UserModel.DoesNotExist:
            return Response ("User doesn`t exists!", status=HTTP_400_BAD_REQUEST)
        return Response ("User data updated successfully!", status=HTTP_200_OK)