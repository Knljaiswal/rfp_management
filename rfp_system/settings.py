"""
Django settings for rfp_system project.
"""

from pathlib import Path
import os
from mongoengine import connect
from dotenv import load_dotenv

# 1. Load the .env file immediately
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--d79mdsf_rzrvf5e*a*(g-q3h+w^sw9@y4i+24sf8!3+yj2&x6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # <-- Your app is registered here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rfp_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rfp_system.wsgi.application'


# Database
# Uses SQLite for Django's internal admin (Users/Sessions), 
# but your actual data will go to MongoDB via MongoEngine.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# --- MongoDB Connection Debugging ---
print("\n--- DEBUGGING DATABASE CONNECTION ---")
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    print("❌ ERROR: MONGO_URI is None. The .env file is not being read.")
    print("   Make sure .env is in the same folder as manage.py")
else:
    # Print only first 25 chars to keep password safe but verify it's loaded
    print(f"🔍 URI found: {mongo_uri[:25]}...") 
    
    try:
        # We force a connection check immediately
        connect(host=mongo_uri)
        print("✅ MongoDB Connection Successful!")
    except Exception as e:
        print(f"❌ Connection Crash: {e}")
print("-------------------------------------\n")

# --- EMAIL SETTINGS (CONSOLE MODE) ---
# This prints emails to the terminal instead of actually sending them.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = 'my-fake-email@company.com'