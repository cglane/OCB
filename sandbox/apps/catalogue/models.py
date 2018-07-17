# yourproject/catalogue/models.py

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from oscar.apps.catalogue.abstract_models import AbstractAttributeOption

class AttributeOption(AbstractAttributeOption):
    image = models.ImageField(_('Image'), upload_to=settings.OSCAR_IMAGE_FOLDER, blank=True,
                              null=True, max_length=255)


from oscar.apps.catalogue.models import *