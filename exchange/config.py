import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'bchbe@gmail.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
