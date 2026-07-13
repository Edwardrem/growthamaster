from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, ['127.0.0.1', 'localhost']),
    EMAIL_PORT=(int, 465),
    EMAIL_USE_SSL=(bool, True),
    EMAIL_USE_TLS=(bool, False),
)
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-me')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
# Deployment host/domain — always allowed regardless of .env
for _host in ('187.55.227.159', 'growthmastersolutions.com', 'www.growthmastersolutions.com'):
    if _host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_host)

# Trusted origins for CSRF-protected POST forms served over the deployment host
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS', default=[
    'http://187.55.227.159:8000',
    'http://187.55.227.159',
    'http://growthmastersolutions.com',
    'https://growthmastersolutions.com',
    'http://www.growthmastersolutions.com',
    'https://www.growthmastersolutions.com',
])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # Project apps
    'core',
    'services',
    'portfolio',
    'contacts',
    'subscribers',
    'email_broadcast',
    'accounts',
    'manage_portal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'manage_portal.middleware.ManagePortalLoginMiddleware',
]

ROOT_URLCONF = 'growthmaster.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'growthmaster.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='127.0.0.1'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Harare'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static/media storage — WhiteNoise serves compressed, hashed static files
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

# Auth
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/manage/'
LOGOUT_REDIRECT_URL = '/'

# Session — 30 minute timeout, reset on activity
SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.titan.email')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_SSL = env('EMAIL_USE_SSL')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='GrowthMaster <noreply@example.com>')
ADMIN_EMAIL = env('ADMIN_EMAIL', default='')
BASE_URL = env('BASE_URL', default='http://127.0.0.1:8000')

# Seeded portal accounts (used by the /seed endpoint) — sourced from .env
SEED_ADMIN_USERNAME = env('ADMIN_USERNAME', default='admin')
SEED_ADMIN_PASSWORD = env('ADMIN_PASSWORD', default='admin1234')
SEED_STAFF_USERNAME = env('STAFF_USERNAME', default='staff')
SEED_STAFF_PASSWORD = env('STAFF_PASSWORD', default='staff1234')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
