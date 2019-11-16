import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        b'\xf296\xe8U\x06\xf4\x95\xabA=e\xd9b*\xe5'

    MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment', 'host' : 'mongodb://localhost:27017/UTA_Enrollment' }