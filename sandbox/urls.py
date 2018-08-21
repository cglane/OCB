import django
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views
from oscar.views import handler403, handler404, handler500

from apps.gateway import urls as gateway_urls
from apps.sitemaps import base_sitemaps
from apps.app import application
from apps.order.app import application as orderApp
from apps.promotions.views import FabricOptionsView, HomeView, AboutPageView, FaqPageView

admin.autodiscover()

urlpatterns = [
    # Include admin as convenience. It's unsupported and only included
    # for developers.
    url(r'^admin/', include(admin.site.urls)),

    # i18n URLS need to live outside of i18n_patterns scope of Oscar
    url(r'^i18n/', include(django.conf.urls.i18n)),
    # Duplicates for en-us
    url(r'^en-us/fabrics', FabricOptionsView.as_view()),
    url(r'^en-us/about', AboutPageView.as_view()),
    url(r'en-us/faqs', FaqPageView.as_view()),
    url(r'^en-us/$', HomeView.as_view()),
    # Non-Duplicates
    url(r'^fabrics', FabricOptionsView.as_view()),
    url(r'^about', AboutPageView.as_view()),
    url(r'faqs', FaqPageView.as_view()),
    # include a basic sitemap
    url(r'^sitemap\.xml$', views.index,
        {'sitemaps': base_sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', views.sitemap,
        {'sitemaps': base_sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]
# Prefix Oscar URLs with language codes
urlpatterns += i18n_patterns(
    # Custom functionality to allow dashboard users to be created
    url(r'gateway/', include(gateway_urls)),
      # PayPal Express integration...
    # Add a path so suppliers can update order status
    url(r'^orders/', include(orderApp.urls)),
    ###Test URL
    url(r'^', application.urls),
)

if settings.DEBUG:
    import debug_toolbar
    # Server statics and uploaded media
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # Allow error pages to be tested
    urlpatterns += [
        url(r'^403$', handler403),
        url(r'^404$', handler404),
        url(r'^500$', handler500),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
