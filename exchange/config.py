import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:PASSWORD@localhost/mydb']
    DEBUG = True
    MAIL_PASSWORD = 'GMAIL_PASSWORD'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'buckscountyhomebrewexchange@gmail.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
