
from django.core.management.base import BaseCommand
from oscar.core.loading import get_model
from django.conf import settings
import csv

ProductCategory = get_model('catalogue', 'ProductCategory')

class Command(BaseCommand):
	def dump(self, qs, outfile_path):
		model = qs.model
		writer = csv.writer(open(outfile_path, 'w'))

		headers = []

		for field in model._meta.fields:
			headers.append((field.name, field.related_model))
		writer.writerow([x[0] for x in headers])


		for obj in qs:
			row = []
			for field in headers:
				print (field, 'field')
				if field[1]:
					rel_obj = getattr(obj, field[0])
					if rel_obj:
						val = getattr(obj, field[0]).id
					else:
						val = ''
				else:
					val = getattr(obj, field[0])
					if callable(val):
						val = val()
				row.append(val)
			writer.writerow(row)
	def handle(self, *args, **options):
		if getattr(settings,'DATABASES')['default']['ENGINE'] != 'django.db.backends.postgresql':
			raise Exception("Database not set google")

		qs = ProductCategory.objects.all()
		outfile_path = 'exports/ProductCategory.csv'

		self.dump(qs, outfile_path)