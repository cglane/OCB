import os
import environ
import oscar

env = environ.Env()

# Path helper
location = lambda x: os.path.join(
   os.path.dirname(os.path.realpath(__file__)), x)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

##To Put in Production
# DEBUG=False
# USE_LESS=False
# STATIC_URL='GOOGLE'
#Allowed Hosts

DEBUG = False
SQL_DEBUG = DEBUG
TEMPLATE_DEBUG = DEBUG
FONTAWESOME_CSS_URL = 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'

ALLOWED_HOSTS = ['localhost','bedswing-app.z8dwrjikpc.us-east-1.elasticbeanstalk.com', '.originalcharlestonbedswing.com']

# Change when in production
DOMAIN = 'https://www.originalcharlestonbedswing.com/'
# DOMAIN = 'https://backend-dot-brave-standard-180615.appspot.com/'
# This is needed for the hosted version of the sandbox
ADMINS = (
   ('Charles Lane', 'charleslane23@gmail.com')
)
###Change in production
if DEBUG == True:
    CONFIRMATION_EMAIL_LIST = ['charleslane23@gmail.com', 'charles@mailinator.com']
else:
    CONFIRMATION_EMAIL_LIST = ['charleslane23@gmail.com', 'bstone443@gmail.com','stephaniejprice@comcast.net' ]

MASTER_EMAIL = 'charleslane23@gmail.com'
ADMIN_EMAIL_ADDRESS = 'bstone443@gmail.com'

EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_HOST_USER = 'info@originalcharlestonbedswing.com'
EMAIL_HOST_PASSWORD = '@Decamp1955!'
EMAIL_PORT = 80
EMAIL_SUBJECT_PREFIX = '[Original Bedswing] '
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
###Needs to be changed to barbara 's email
MANAGERS = ADMINS
SHOW_TAX_CHECKOUT = True
if DEBUG == False:
   STRIPE_SECRET_KEY = os.environ.get('BEDSWING_STRIPE_SECRET_KEY')
   STRIPE_PUBLIC_KEY = os.environ.get('BEDSWING_STRIPE_PUBLIC_KEY')
else:
   STRIPE_SECRET_KEY = 'sk_test_l35XYUB28ffo5jx8JP7yB2Y2'
   STRIPE_PUBLIC_KEY = 'pk_test_lWSwsHlK2F8sdEYOpDm1bdSh'

SECRET_KEY = '9%d9&5!^+hcq!pin#0lfz(qj8j2h7y$p*rr-o#cy+)9%dyvwkn'

ABOUT_PAGE_IMAGE = 'couple-out-west.jpg'
LANDING_PAGE_MAIN_IMAGE = {'img': 'original-magazine.jpg', 'caption': ''}
LANDING_PAGE_IMAGES = {
    '2':{'img':'bedswing-pool-dark.jpg', 'caption':"Each bedswing is crafted with love by veteran woodworkers. "},
    '1':{'img':'bedswing-cushions.jpg','caption': "We use quality, furniture-grade cypress and mahogany."},
    '5':{'img':'bedswing-fan-porch.jpg','caption': "The fabrics used for our cushions and pillows are Outdura products, known industry wide for their comfort and durability."},
    '0':{'img':'couple-out-west.jpg','caption':''},
    '4':{'img':'bedswing-pool-light.jpg','caption': ''},
    '3':{'img':'double-bedswing-white.jpg', 'caption': ''}
}
LANDING_PAGE_BEDSWING_OPTIONS = [
    # {
    #     'img': 'clear-coat-mahogany.jpg',
    #     'caption': 'Clear Coat Mahogany'
    # },
    {
        'img': 'clear-coat-cypress.jpg',
        'caption': 'Clear Coat Cypress'
    },
    {
        'img': 'custom-color.jpg',
        'caption': 'Custom Color'
    },
    {
        'img': 'mahogany-finish.jpg',
        'caption': 'Mahogany Finish'
    },
    {
        'img': 'painted-black.jpg',
        'caption': 'Painted Black'
    },
    {
        'img': 'painted-white.jpg',
        'caption': 'Painted White'
    }



]
LANDING_PAGE_FABRIC_OPTIONS = [
    {
        'img': 'solid-fabrics-1.jpg',
        'caption': 'Solid Fabrics One'
    },
    {
        'img': 'solid-fabrics-2.jpg',
        'caption': 'Solid Fabrics Two'
    },
    {
        'img': 'solid-fabrics-3.jpg',
        'caption': 'Solid Fabrics Three'
    },
    {
        'img': 'jaquards-fabrics.jpg',
        'caption': 'Jaquards Fabrics'
    },
    {
        'img': 'com.jpg',
        'caption': 'COM'
    },
    {
        'img': 'striped-fabrics.jpg',
        'caption': 'Striped Fabrics'
    }
]

SHIPPING_RATES = { "AK" : 775,
               "AL": 425,
               "AR": 425,
               "AS": 775,
               "AZ": 550,
               "CA": 775,
               "CO": 550,
               "CT": 525,
               "DC": 425,
               "DE": 425,
               "FL": 425,
               "GA": 375,
               "GU": 775,
               "HI": 775,
               "IA": 475,
               "ID": 550,
               "IL": 400,
               "IN": 400,
               "KS": 450,
               "KY": 400,
               "LA": 425,
               "MA": 525,
               "MD": 375,
               "ME": 575,
               "MI": 500,
               "MN": 550,
               "MO": 400,
               "MS": 400,
               "MT": 550,
               "NC": 375,
               "ND": 575,
               "NE": 575,
               "NH": 550,
               "NJ": 550,
               "NM": 550,
               "NV": 775,
               "NY": 550,
               "OH": 400,
               "OK": 525,
               "OR": 775,
               "PA": 525,
               "PR": 1000,
               "RI": 525,
               "SC": 275,
               "SD": 550,
               "TN": 400,
               "TX": 525,
               "UT": 550,
               "VA": 375,
               "VI": 1000,
               "VT": 550,
               "WA": 775,
               "WI": 550,
               "WV": 325,
               "WY": 550,
                "TE": 50}

ONLY_CUSHIONS_DEDUCTION = 50
SALES_TAX = '0.09'

# Use a Sqlite database by default
if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ebdb',
            'USER': os.environ.get('BEDSWING_POSTGRES_USER'),
            'PASSWORD': os.environ.get('BEDSWING_POSTGRES_PASSWORD'),
            'HOST': 'aa4nz04daw46y8.c8pgtunfw54j.us-east-1.rds.amazonaws.com',
            'PORT': '5432',
        }
    }

CACHES = {
   'default': env.cache(default='locmemcache://'),
}

# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
# SESSION_COOKIE_NAME = 'my_cookie'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
USE_TZ = True
TIME_ZONE = 'America/New_York'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
OSCAR_ABOUT_PAGE='about'
# Includes all languages that have >50% coverage in Transifex
# Taken from Django's default setting for LANGUAGES
gettext_noop = lambda s: s
LANGUAGES = (
   ('en-us', gettext_noop('American English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_BEDSWING_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_BEDSWING_KEY')
AWS_STORAGE_BUCKET_NAME = 'bedswing-bucket'
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


MEDIAFILES_LOCATION = 'media'
MEDIA_ROOT = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

DEFAULT_FILE_STORAGE = 'settings.storage_backends.MediaStorage'  # <-- here is where we reference it

STATICFILES_FINDERS = (
   'django.contrib.staticfiles.finders.FileSystemFinder',
   'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.

TEMPLATES = [
   {
       'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [
           os.path.join(BASE_DIR, "templates"),
           oscar.OSCAR_MAIN_TEMPLATE_DIR,
       ],
       'OPTIONS': {
           # 'loaders': [
		   #
           #     'django.template.loaders.filesystem.Loader',
           #     'django.template.loaders.app_directories.Loader',
           #     'django.template.loaders.eggs.Loader'
           #     ,
           # ],
           'loaders': [
               ('django.template.loaders.cached.Loader', [
                   'django.template.loaders.filesystem.Loader',
               'django.template.loaders.app_directories.Loader',
               'django.template.loaders.eggs.Loader'
                   ]),
           ],
           'context_processors': [
               'django.contrib.auth.context_processors.auth',
               'django.template.context_processors.request',
               'django.template.context_processors.debug',
               'django.template.context_processors.i18n',
               'django.template.context_processors.media',
               'django.template.context_processors.static',
               'django.contrib.messages.context_processors.messages',

               # Oscar specific
               'oscar.apps.search.context_processors.search_form',
               'oscar.apps.customer.notifications.context_processors.notifications',
               'oscar.apps.promotions.context_processors.promotions',
               'oscar.apps.checkout.context_processors.checkout',
               'oscar.core.context_processors.metadata',
               'apps.checkout.checkout_vars_two.checkout'
           ],
           'debug': DEBUG,
       }
   }
]

MIDDLEWARE = [
   'debug_toolbar.middleware.DebugToolbarMiddleware',

   'django.middleware.security.SecurityMiddleware',
   'whitenoise.middleware.WhiteNoiseMiddleware',
   'django.middleware.csrf.CsrfViewMiddleware',

   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.contrib.auth.middleware.AuthenticationMiddleware',
   'django.contrib.messages.middleware.MessageMiddleware',
   'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

   # Allow languages to be selected
   'django.middleware.locale.LocaleMiddleware',
   'django.middleware.http.ConditionalGetMiddleware',
   'django.middleware.common.CommonMiddleware',

   # Ensure a valid basket is added to the request instance for every request
   'oscar.apps.basket.middleware.BasketMiddleware',
   ## Page Refresh
   #'livereload.middleware.LiveReloadScript'
]

ROOT_URLCONF = 'urls'
DEBUG_TOOLBAR_CONFIG = {
   # Add in this line to disable the panel
   'DISABLE_PANELS': {
       'debug_toolbar.panels.templates.TemplatesPanel',
       'debug_toolbar.panels.redirects.RedirectsPanel',
   },
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
   'version': 1,
   'disable_existing_loggers': True,
   'formatters': {
       'verbose': {
           'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
       },
       'simple': {
           'format': '[%(asctime)s] %(message)s'
       },
   },
   'root': {
       'level': 'DEBUG',
       'handlers': ['console'],
   },
   'handlers': {
       'null': {
           'level': 'DEBUG',
           'class': 'logging.NullHandler',
       },
       'console': {
           'level': 'DEBUG',
           'class': 'logging.StreamHandler',
           'formatter': 'simple'
       },
   },
   'loggers': {
       'oscar': {
           'level': 'DEBUG',
           'propagate': True,
       },
       'oscar.catalogue.import': {
           'handlers': ['console'],
           'level': 'INFO',
           'propagate': False,
       },
       'oscar.alerts': {
           'handlers': ['null'],
           'level': 'INFO',
           'propagate': False,
       },

       # Django loggers
       'django': {
           'handlers': ['null'],
           'propagate': True,
           'level': 'INFO',
       },
       'django.request': {
           'handlers': ['console'],
           'level': 'ERROR',
           'propagate': True,
       },
       'django.db.backends': {
           'level': 'WARNING',
           'propagate': True,
       },
       'django.security.DisallowedHost': {
           'handlers': ['null'],
           'propagate': False,
       },

       # Third party
       'raven': {
           'level': 'DEBUG',
           'handlers': ['console'],
           'propagate': False,
       },
       'sorl.thumbnail': {
           'handlers': ['console'],
           'propagate': True,
           'level': 'INFO',
       },
   }
}


INSTALLED_APPS = [
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.sites',
   'django.contrib.messages',
   'django.contrib.admin',
   'django.contrib.flatpages',
   'django.contrib.staticfiles',
   'django.contrib.sitemaps',
   'django_extensions',
   'djangosecure',
   # Debug toolbar + extensions
   #'livereload',
   'fontawesome',
   'debug_toolbar',
   'apps.gateway',
    # For allowing dashboard access
   'widget_tweaks',
    'storages',
                 ] + oscar.get_core_apps([
   'apps.future',
   'apps.basket',
   'apps.catalogue',
   'apps.checkout',
   'apps.order',
   'apps.partner',
   'apps.shipping',
   'apps.dashboard.communications',
   'apps.dashboard.orders',
   'apps.promotions',
])

# AUTH_USER_MODEL = "user.UseExtendedUserModelr"

# Add Oscar's custom auth backend so users can sign in using their email
# address.
AUTHENTICATION_BACKENDS = (
   'oscar.apps.customer.auth_backends.EmailBackend',
   'django.contrib.auth.backends.ModelBackend',
)




AUTH_PASSWORD_VALIDATORS = [
   {
       'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
       'OPTIONS': {
           'min_length': 9,
       }
   },
   {
       'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
   },
]

LOGIN_REDIRECT_URL = '/'
APPEND_SLASH = True

# ====================
# Messages contrib app
# ====================

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
   messages.ERROR: 'danger'
}

# Haystack settings
HAYSTACK_CONNECTIONS = {
   'default': {
       'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
       'PATH': location('whoosh_index'),
   },
}
# Here's a sample Haystack config if using Solr (which is recommended)
#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#        'URL': u'http://127.0.0.1:8983/solr/oscar_latest/',
#        'INCLUDE_SPELLING': True
#    },
#}

###In Env file
# =============
# Debug Toolbar
# =============

INTERNAL_IPS = ['127.0.0.1', '::1']

# ==============
# Oscar settings
# ==============

from oscar.defaults import *

###Required Fields
OSCAR_REQUIRED_ADDRESS_FIELDS = ('first_name', 'last_name', 'line1',
                                'line4', 'postcode', 'country', 'state')
##Emails
OSCAR_FROM_EMAIL="Original Charleston Bedswing <bstone443@gmail.com>"
DEFAULT_FROM_EMAIL="Original Charleston Bedswing <bstone443@gmail.com>"

# Meta
# ====
OSCAR_DEFAULT_CURRENCY = 'USD'

OSCAR_SHOP_TAGLINE = 'Charleston Bedswing'
OSCAR_SHOP_NAME = 'Original'

# Add Payflow dashboard stuff to settings
from django.utils.translation import ugettext_lazy as _
OSCAR_DASHBOARD_NAVIGATION.append({
   'label': _('Stripe'),
   'icon': 'icon-globe',
   'children': [
       {
           'label': _('Stripe transactions'),
           'url_name': 'stripe-list',
       },
   ]
})
OSCAR_RECENTLY_VIEWED_PRODUCTS = 20
OSCAR_ALLOW_ANON_CHECKOUT = True

# This is added to each template context by the core context processor.  It is
# useful for test/stage/qa sites where you want to show the version of the site
# in the page title.
DISPLAY_VERSION = False


# Order processing
# ================

# Sample order/line status settings. This is quite simplistic. It's like you'll
# want to override the set_status method on the order object to do more
# sophisticated things.
OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'

# This dict defines the new order statuses than an order can move to
OSCAR_ORDER_STATUS_PIPELINE = {
   'Pending': ('Being processed', 'Cancelled',),
   'Being processed': ('Complete', 'Cancelled',),
   'Cancelled': (),
   'Complete': (),
}
OSCAR_LINE_STATUS_PIPELINE = {
   'Pending': ('received', 'shipped', 'cancelled'),
   'received': ('shipped',  'cancelled'),
   'shipped': ('cancelled','received'),
   'cancelled': ()
}
# This dict defines the line statuses that will be set when an order's status
# is changed
OSCAR_ORDER_STATUS_CASCADE = {
   'Being processed': 'Being processed',
   'Cancelled': 'Cancelled',
   'Cancelled': 'Cancelled',
   'Complete': 'Shipped',
}

# LESS/CSS
# ========

# We default to using CSS files, rather than the LESS files that generate them.
# If you want to develop Oscar's CSS, then set USE_LESS=True to enable the
# on-the-fly less processor.
USE_LESS = False


# Sentry
# ======

if env('SENTRY_DSN', default=None):
   RAVEN_CONFIG = {'dsn': env('SENTRY_DSN', default=None)}
   LOGGING['handlers']['sentry'] = {
       'level': 'ERROR',
       'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
   }
   LOGGING['root']['handlers'].append('sentry')
   INSTALLED_APPS.append('raven.contrib.django.raven_compat')


# Sorl
# ====

THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_KEY_PREFIX = 'bedswing'
THUMBNAIL_KVSTORE = env(
   'THUMBNAIL_KVSTORE',
   default='sorl.thumbnail.kvstores.cached_db_kvstore.KVStore')
THUMBNAIL_REDIS_URL = env('THUMBNAIL_REDIS_URL', default=None)


# Django 1.6 has switched to JSON serializing for security reasons, but it does not
# serialize Models. We should resolve this by extending the
# django/core/serializers/json.Serializer to have the `dumps` function. Also
# in tests/config.py
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
# Try and import local settings which can be used to override any of the above.

##Live reload
try:
   from settings_local import *
except ImportError:
   pass

