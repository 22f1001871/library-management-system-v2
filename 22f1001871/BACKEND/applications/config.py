'''
class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///DATABASE.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'mysecretkey'
    SECURITY_PASSWORD_SALT = 'mysecuritypasswordsalt'
       
    CELERY_BROKER_URL = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://localhost:6379"
    CELERY_IMPORTS = ('applications.task',)
    
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379

    CELERY_TIMEZONE = 'Asia/Kolkata'
    CELERY_ENABLE_UTC = False
'''
import os

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///DATABASE.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'mysecuritypasswordsalt')
    
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
    CELERY_IMPORTS = ('applications.task',)
    
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))
    CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST', 'localhost')
    CACHE_REDIS_PORT = int(os.getenv('CACHE_REDIS_PORT', 6379))

    CELERY_TIMEZONE = 'Asia/Kolkata'
    CELERY_ENABLE_UTC = False