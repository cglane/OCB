from django.core.management.base import BaseCommand
from oscar.core.loading import get_model
from django.core.files.base import ContentFile
from django.conf import settings
import ast
import csv
AttributeOptionGroup = get_model('catalogue', 'AttributeOptionGroup')
ProductClass = get_model('catalogue', 'ProductClass')
Category = get_model('catalogue', 'Category')
Product = get_model('catalogue', 'Product')
Partner = get_model('partner', 'Partner')
Basket = get_model('basket', 'Basket')
Line = get_model('basket', 'Line')
Option = get_model('catalogue', 'Option')
StockRecord = get_model('partner', 'StockRecord')
ShippingAddress = get_model('address', 'UserAddress')
from django.contrib.sites.models import Site
file_upload = {
	'address': [
		'Country'
	],
	'catalogue':[
		# 'Option',
		# 'Category',
		# 'ProductClass',
		# 'AttributeOptionGroup',
		# 'AttributeOption',
		# 'Product',
		'ProductImage',
		'ProductCategory'

	],
	'partner': [
		'Partner',
		'StockRecord'
	],
	# 'basket': [
	# 	'Basket',
	# 	'Line',
	# 	'LineAttribute',
	# ],
	# 'order': [
	# 	'Order',
	# 	'OrderDiscount'
	# ],
	'customer': [
		'CommunicationEventType'
	]

}
image_base = './bedswing-bucket/'


class Command(BaseCommand):
	def get_list(self, file_path):
		my_list = []
		with open(file_path) as csvfile:
			reader = csv.DictReader(csvfile)
			for item in reader:
				my_list.append(item)
			csvfile.close()
		return my_list

	def upload_model(self, Model, model_name):
		my_list = self.get_list('exports/'+ model_name + '.csv')
		for item in my_list:
			##Country model is very particular
			if model_name == 'Country':
				item_exists = Model.objects.filter(name=item['name'])
			else:
				item_exists = Model.objects.filter(id=item['id'])
			# Prevent Duplicates
			if not item_exists:
				local_obj = Model()
			else:
				local_obj = item_exists[0]


			img_path = ''
			resale_path = ''
			original_path = ''
			parent_group = None
			for key in item.keys():
				##Check if it is an image and if there is any content
				if key == 'image' and item[key]:
					img_path = item[key]
				if key == 'original':
					original_path = item[key]
				elif key == 'resale_certificate' and item[key]:
					resale_path = item[key]
					print (resale_path, 'resale path')
				elif key == 'categories':
					pass
				# elif key == 'category':
				# 	cat = Category.objects.get(id=item[key])
				# 	local_obj.category = cat
				elif key == 'product_options':
					options = ast.literal_eval(item[key])
					for it in options:
						option = Option.objects.get(id=it)
						print (option, 'option')
						local_obj.product_options.add(option)
				elif not item[key]:
					pass
				elif key == 'owner':
					pass
				elif key == 'shipping_address':
					shipping_address = ShippingAddress.objects.filter(line1 = item[key])
					if shipping_address:
						local_obj.shipping_address = shipping_address[0]
					else:
						shipping_address = ShippingAddress(line1 = item[key], country_id=1).save()
						local_obj.shipping_address = shipping_address
				elif key == 'site':
					site = Site.objects.all()[0]
					local_obj.site = site
				elif key == 'line':
					line = Line.objects.get(id=item[key])
					local_obj.line = line
				elif key == 'basket':
					basket = Basket.objects.get(id=item[key])
					local_obj.basket = basket
				elif key == 'stockrecord':
					stockrecord = StockRecord.objects.get(id=item[key])
					local_obj.stockrecord = stockrecord
				elif key == 'group':
					group = AttributeOptionGroup.objects.get(id=item[key])
					local_obj.group = group
				elif key == 'product_class':
					product_class = ProductClass.objects.get(id=item[key])
					local_obj.product_class = product_class
				elif key == 'product':
					product = Product.objects.get(id=item[key])
					local_obj.product = product
				elif key == 'partner':
					partner = Partner.objects.get(id=item[key])
					local_obj.partner = partner
				else:
					setattr(local_obj, key, item[key])
			local_obj.save()

			## Need to add Image after record is created
			if img_path:
				img_src = image_base + img_path
				print (img_src, 'src')
				name = img_path.split('/')[-1]
				print (name, 'name')
				with open(img_src, 'rb') as f:
					data = f.read()
				local_obj.image.save(name, ContentFile(data))
				local_obj.save()
			if original_path:
				img_src = image_base + original_path
				print (img_src, 'src')
				name = img_src.split('/')[-1]
				print (name, 'name')
				with open(img_src, 'rb') as f:
					data = f.read()
				local_obj.original.save(name, ContentFile(data))
				local_obj.save()
			if resale_path:
				resale_path = image_base + resale_path
				print (resale_path, 'src')
				name = resale_path.split('/')[-1]
				with open(resale_path) as f:
					data = f.read()
				local_obj.resale_certificate.save(name, ContentFile(data))
				local_obj.save()

	def handle(self, *args, **options):
		if getattr(settings,'DATABASES')['default']['ENGINE'] == 'django.db.backends.postgresql':
			raise Exception("Database set as google")
		group = 'customer'
		for item in file_upload[group]:
			print (item, ': model')
			Model = get_model(group, item)
			self.upload_model(Model, item)

