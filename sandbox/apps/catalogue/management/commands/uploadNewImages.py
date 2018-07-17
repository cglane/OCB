from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from oscar.core.loading import get_model
from django.conf import settings
import csv
import os
ProductAttribute = get_model('catalogue', 'AttributeOption')
file_path = '../fabric_images'
class Command(BaseCommand):
    	def handle(self, *args, **options):
            new_images = os.listdir(file_path)
            product_attributes = ProductAttribute.objects.all()
            for item in product_attributes:
                item_name = ''.join(item.option.split(' ')) + '.jpg'
                if item_name in new_images:
                    print (item_name, 'in there')
                    img_src = file_path + '/' + item_name
                    with open(img_src, 'rb') as f:
					    data = f.read()
                    print(img_src, 'src')
                    item.image.save(item_name, ContentFile(data))
                    item.save()
                else:
                    print(item_name, 'not in there')

            