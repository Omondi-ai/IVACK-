import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables
load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# Security Settings
# ========================
SECRET_KEY = os.getenv('SECRET_KEY', os.getenv('DJANGO_SECRET_KEY', 'change-me-in-prod'))
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Default to False in production

# AWS-specific hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'web']
AWS_DOMAIN = os.getenv('AWS_DOMAIN')  # Will be set in EB/Lightsail
if AWS_DOMAIN:
    ALLOWED_HOSTS.extend([
        AWS_DOMAIN,
        f'*.{AWS_DOMAIN}',  # For subdomains
        '.elasticbeanstalk.com',  # For EB
        '.amazonaws.com'  # For AWS generally
    ])

CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
if AWS_DOMAIN:
    CSRF_TRUSTED_ORIGINS.extend([
        f'https://{AWS_DOMAIN}',
        f'https://*.{AWS_DOMAIN}'
    ])

# ======================== [Rest of your original settings remain the same until database] ========================

# ========================
# Database Configuration - AWS Optimized
# ========================
if os.getenv('AWS_RDS_HOST'):  # If using AWS RDS
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('AWS_RDS_DB_NAME'),
            'USER': os.getenv('AWS_RDS_USERNAME'),
            'PASSWORD': os.getenv('AWS_RDS_PASSWORD'),
            'HOST': os.getenv('AWS_RDS_HOST'),
            'PORT': os.getenv('AWS_RDS_PORT', '5432'),
        }
    }
else:  # Fallback to your original config
    DATABASES = {
        'default': dj_database_url.config(
            default='postgres://django_admin:postgres@db:5432/university_portal',
            conn_max_age=600
        )
    }

# ========================
# Channels Configuration - AWS Optimized
# ========================
if os.getenv('AWS_REDIS_HOST'):  # If using AWS ElastiCache
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(os.getenv('AWS_REDIS_HOST'), 6379)],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }

# ========================
# Static Files - AWS Optimized
# ========================
if os.getenv('AWS_STORAGE_BUCKET_NAME'):  # If using S3
    AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_REGION', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_DIRS = [BASE_DIR / 'static']
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# [Rest of your original settings remain the same]