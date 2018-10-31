import logging
from logging.handlers import RotatingFileHandler

def logf():
    logger = logging.getLogger('myLogger')
    logger.setLevel(logging.ERROR)
        # logging.basicConfig(filename='log_file.log',
        #                     level=logging.DEBUG,        #filemode='w'
        #                     format='%(asctime)s  %(levelname)s:%(message)s',
        #                     datefmt='%m/%d/%Y %I:%M:%S %p' )
    formatter = logging.Formatter('%(asctime)s : %(pathname)s(%(lineno)d) : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        # %(pathname)s Full pathname of the source file where the logging call was issued(if available).
        #
        # %(filename)s Filename portion of pathncd ame.
        #
        # %(module)s Module (name portion of filename).
        #
        # %(funcName)s Name of function containing the logging call.
        #
        # %(lineno)d Source line number where the logging call was issued (if available).
    handler = RotatingFileHandler('test_log.log', maxBytes=300, backupCount=10)
    handler.setFormatter(formatter)
    if (logger.hasHandlers()):
        logger.handlers.clear()
    logger.addHandler(handler)
    # logger.removeHandler (handler)

    handler.setLevel(logging.DEBUG)
    return logger

# logger=logf()
#
# for i in range(100):
#     logger.debug("test number is:{}".format(i))

#  C:\Users\GSC-30308\PycharmProjects\Pro1\venv\Scripts
# activate
# python manage.py makemigrations migrate runserver

# disable_existing_loggers=True

