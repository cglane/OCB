from django.db import models
import requests

from oscar.apps.basket.abstract_models import AbstractBasket

class Basket(AbstractBasket):
    resale_certificate = models.FileField(upload_to="uploads/")
    def file_link(self):
        if self.resale_certificate:
            request = requests.get(self.resale_certificate.url)
            if request.status_code == 200:
                return "<a href='%s' download>%s</a>" % (self.resale_certificate.url,self.resale_certificate.name)
        return "No attachment"

from oscar.apps.basket.models import *

