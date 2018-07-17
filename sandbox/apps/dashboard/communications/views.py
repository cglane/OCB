from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template import TemplateSyntaxError
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.conf import settings

from oscar.core.loading import get_class, get_model

CommunicationEventType = get_model('customer', 'CommunicationEventType')
CommunicationEventTypeForm = get_class('dashboard.communications.forms',
                                       'CommunicationEventTypeForm')
Dispatcher = get_class('customer.utils', 'Dispatcher')
Order = get_model('order', 'Order')

class ListView(generic.ListView):
    model = CommunicationEventType
    template_name = 'dashboard/comms/list.html'
    context_object_name = 'commtypes'


class UpdateView(generic.UpdateView):
    model = CommunicationEventType
    form_class = CommunicationEventTypeForm
    template_name = 'dashboard/comms/detail.html'
    context_object_name = 'commtype'
    success_url = '.'
    slug_field = 'code'

    def form_invalid(self, form):
        messages.error(self.request,
                       _("The submitted form was not valid, please correct "
                         "the errors and resubmit"))
        return super(UpdateView, self).form_invalid(form)

    def form_valid(self, form):
        if 'send_preview' in self.request.POST:
            return self.send_preview(form)
        if 'show_preview' in self.request.POST:
            return self.show_preview(form)
        messages.success(self.request, _("Email saved"))
        return super(UpdateView, self).form_valid(form)

    def get_messages_context(self, form):
        order_id = form.cleaned_data['preview_order_number']
        order = Order.objects.filter(number=order_id)[0]
        line = order.lines.all()[0]
        ctx = {
            'order': order,
            'line': line,
            'user': self.request.user,
            'site': get_current_site(self.request),
            'domain': getattr(settings, 'DOMAIN'),
            'received_url': getattr(settings, 'DOMAIN') + 'orders/update/' + str(line.id) + '/received',
            'shipped_url': getattr(settings, 'DOMAIN') + 'orders/update/' + str(line.id) + '/shipped',
               }
        return ctx

    def show_preview(self, form):
        ctx = super(UpdateView, self).get_context_data()
        ctx['form'] = form

        commtype = form.save(commit=False)
        commtype_ctx = self.get_messages_context(form)
        try:
            msgs = commtype.get_messages(commtype_ctx)
        except TemplateSyntaxError as e:
            form.errors['__all__'] = form.error_class([six.text_type(e)])
            return self.render_to_response(ctx)

        ctx['show_preview'] = True
        ctx['preview'] = msgs
        return self.render_to_response(ctx)

    def send_preview(self, form):
        ctx = super(UpdateView, self).get_context_data()
        ctx['form'] = form
        commtype = form.save(commit=False)
        commtype_ctx = self.get_messages_context(form)
        try:
            msgs = commtype.get_messages(commtype_ctx)
        except TemplateSyntaxError as e:
            form.errors['__all__'] = form.error_class([six.text_type(e)])
            return self.render_to_response(ctx)

        email = form.cleaned_data['preview_email']
        dispatch = Dispatcher()
        dispatch.send_email_messages(email, msgs)
        messages.success(self.request,
                         _("A preview email has been sent to %s") % email)

        return self.render_to_response(ctx)
