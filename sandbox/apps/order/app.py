from django.conf.urls import url

from oscar.apps.catalogue.reviews.app import application as reviews_app
from oscar.core.application import Application
from oscar.core.loading import get_class

class OrderApplication(Application):
    name = 'orders'
    update_view = get_class('order.views', 'UpdateView')
    def get_urls(self):
        urls = [
            url(r'^update/(?P<id>\d+)/(?P<status>[\w-]+)/$', self.update_view.as_view(), name='update'),
        ]
        return self.post_process_urls(urls)


application = OrderApplication()