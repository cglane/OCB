from django.core.management.base import BaseCommand
import unittest
from oscar.core.loading import get_class, get_model
OrderPlacementMixin = get_class('checkout.views', 'OrderPlacementMixin')
Order = get_model('order', 'Order')
Partner = get_model('partner', 'partner')
Line = get_model('order', 'Line')

class Command(BaseCommand):
    help = """
    If you need Arguments, please check other modules in 
    django/core/management/commands.
    """

    def handle(self, **options):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestChronology)
        unittest.TextTestRunner().run(suite)


class TestChronology(unittest.TestCase):
    def setUp(self):
        print "Write your pre-test prerequisites here"

    def test_equality(self):
        orders = Order.objects.all()
        first_order = orders[0]
        print first_order
        response = OrderPlacementMixin().handle_successful_order(first_order)
        print response
        self.assertEqual(response, '200')