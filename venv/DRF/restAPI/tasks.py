from __future__ import absolute_import, unicode_literals
from celery import shared_task
from restAPI.models import UserModel, metadata
import time
import logging
from restAPI.logConf import logf
logger = logf()

@shared_task(name="length_username_new")                   #gets triggered from serializers
def new_user_length():
    # time.sleep(25)
    user = UserModel.objects.last()                        #fetches data from DB
    user.length = len(user.username)
    logger.info("{}`s userlength is updated in the database".format (user.username))
    user.save() #user.save(['length'])                     #saves data back to the same DB


@shared_task(name="length_username_periodic")   #gets triggered from celery
def user_length():
    queryset1 = UserModel.objects.all()
    queryset2 = metadata.objects.all()
    for i in queryset1:
        if queryset2.filter(username=i.username).exists():
            pass
        else:
            logger.info("Metadata updated!")
            metadata.objects.create(username=i.username, name_length=len(i.username))  #inserts record into "metadata" table
