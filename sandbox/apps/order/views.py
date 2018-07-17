import warnings

from django.contrib import messages
from django.core.paginator import InvalidPage
from django.http import Http404, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, TemplateView

from oscar.apps.catalogue.signals import product_viewed
from oscar.core.compat import user_is_authenticated
from oscar.core.loading import get_class, get_model
from apps.order.utils import CreateCustomMessages
Product = get_model('catalogue', 'product')
Category = get_model('catalogue', 'category')
Line = get_model('order', 'line')

class UpdateView(DetailView):
    def get(self, request, **kwargs):
        if kwargs['id'] and kwargs['status']:
            line_arr = Line.objects.filter(id=kwargs['id'])
            if line_arr:
                try:
                    my_line = line_arr[0]
                    my_line.set_status(kwargs['status'])
                    new_status = my_line.status
                    response = "<h1> Success! </h1>" \
                            "<h2>You have updated the order: %s to a status of: <strong>%s</strong></h2>"\
                            %(my_line.order, new_status)
                    # Email to barbara
                    CreateCustomMessages().send_email(my_line, 'ORDER_STATUS_CHANGE')
                except:

                    response = "<h1> Failure! </h1>" \
                            "Orders must first be set to a status of 'Received' then a status of 'Shipped"

            else:
                response ='Order not Found! Please contact Administrator.'
        return HttpResponse(response)


