from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
import unittest





class Driver(unittest.TestCase):
	def setUp(self):
		self.user1 = {
			'first_name': 'charles',
			'last_name': 'lane',
			'address': '13 Drews Ct.',
			'city': 'charleston',
			'state': 'SC',
			'zip': '29403',
			'country': 'US',
			'phone_number': '8436479951',
			'username': 'charleslane3@gmail.com',
			'email': 'charleslane23@gmail.com',
			'card_number': '4242424242424242',
			'date': '10/25',
			'cvc': '123'

		}
		self.user2 = {
			'first_name': 'juamn',
			'last_name': 'pablo',
			'address': '13 Drews Ct.',
			'city': 'charleston',
			'state': 'TX',
			'zip': '29403',
			'country': 'US',
			'phone_number': '8436479951',
			'username': 'charles@gmail.com',
			'email': 'charles@gmail.com',
			'card_number': '4242424242424242',
			'date': '10/30',
			'cvc': '123'
		}
		self.options = {
			'ceiling_height': '14',
			'striped-fabric': 'Bisto Checkerboard 7036',
			'bedswing-size': 'Original Bedswing',
			'striped-fabrics-piping': 'Capita Admiral 3006',
			'color': 'black'
		}
		self.options_two = {
			'ceiling_height': '14',
			'color': 'black',
			'fabric': 'Avila Cocoa 8378',
			'bedswing-size': 'Original Bedswing',
			'piping': 'Avila Chablis 8385'
		}
		self.options_three = {
			'fabric': 'red',
			'bedswing-size': 'Original Bedswing',
			'piping': 'White Piping'
		}

		self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

	def run_checks(self, total):
		order_total = self.driver.find_element_by_css_selector("h3.price_color").text
		self.assertEqual(order_total, total)



	def checkout(self, user, total):
		# Checkout Now
		self.driver.get('http://localhost:8000/checkout/')
		time.sleep(2)
		# Checkout as guest
		self.driver.find_element_by_id("id_username").send_keys(user['username'])
		self.driver.find_element_by_tag_name("form").submit()
		# Fill in form
		self.driver.find_element_by_id('id_first_name').send_keys(user['first_name'])
		self.driver.find_element_by_id('id_last_name').send_keys(user['last_name'])
		self.driver.find_element_by_id('id_line1').send_keys(user['address'])
		self.driver.find_element_by_id('id_line4').send_keys(user['city'])
		self.driver.find_element_by_id('id_state').send_keys(user['state'])
		self.driver.find_element_by_id('id_postcode').send_keys(user['zip'])
		self.driver.find_element_by_id('id_phone_number').send_keys(user['phone_number'])

		# Submit
		self.driver.find_element_by_id("new_shipping_address").submit()

		# Fill in Stripe
		self.driver.find_element_by_class_name("stripe-button-el").click()
		time.sleep(2)
		self.driver.switch_to.frame('stripe_checkout_app')
		stripe_overlay = self.driver.find_element_by_css_selector('.Modal-animationWrapper')

		inputs = self.driver.find_elements_by_class_name("Fieldset-input")

		# Email
		email_input = inputs[0]
		email_input.send_keys(user['email'])
		email_input.send_keys(Keys.TAB)

		# Card
		card_input = inputs[1]
		card_input.send_keys('4242424242424242')
		time.sleep(0.25)

		# Expiration
		exp_input = inputs[2]
		exp_input.send_keys('08')
		time.sleep(0.25)
		exp_input.send_keys('30')

		# CSV
		csc_input = inputs[3]
		csc_input.send_keys('424')

		time.sleep(0.25)
		self.driver.find_element_by_css_selector("button[type=submit]").click()

		##Submit Order
		self.driver.switch_to_default_content()
		time.sleep(4)

		self.run_checks(total)
		self.driver.find_element_by_id("place_order_form").submit()
		self.driver.quit()
	def test_add_basket(self):
		## As a logout new user
		self.driver.get("http://localhost:8000/catalogue/category/mini-bedswing_9/")

		#Navigate to Clear Mahogany
		self.driver.find_element_by_link_text('Clear Coat Mahogany').click()
		self.driver.find_element_by_xpath("//select[@name='ceiling-height']/option[text()='{0}']"
										  .format(self.options['ceiling_height']))\
											.click()
		#Add Cart
		self.driver.find_element_by_class_name("btn-add-to-basket").click()


		## Navigate to Stripe Fabrics
		self.driver.get("http://localhost:8000/catalogue/striped-fabrics_33/")
		self.driver.find_element_by_xpath("//select[@name='striped-fabrics']/option[text()='{0}']"
										  .format(self.options['striped-fabric']))\
											.click()
		time.sleep(.25)
		self.driver.find_element_by_xpath("//select[@name='bedswing-size']/option[text()='{0}']"
										  .format(self.options['bedswing-size']))\
											.click()
		time.sleep(.25)

		self.driver.find_element_by_xpath("//select[@name='striped-fabrics-piping']/option[text()='{0}']"
										  .format(self.options['striped-fabrics-piping']))\
											.click()
		self.driver.find_element_by_class_name("btn-add-to-basket").click()


		time.sleep(.25)
		self.checkout(total="$4,810.17", user = self.user1)

	def test_add_basket_two(self):
		## As a logout new user
		self.driver.get("http://localhost:8000/catalogue/custom-color_29/")

		# Navigate to Clear Mahogany
		self.driver.find_element_by_xpath("//select[@name='ceiling-height']/option[text()='{0}']"
										  .format(self.options_two['ceiling_height'])) \
			.click()
		self.driver.find_element_by_id("id_custom-color").send_keys(self.options_two['color'])
		# Add Cart
		self.driver.find_element_by_class_name("btn-add-to-basket").click()

		## Navigate to Stripe Fabrics
		self.driver.get("http://localhost:8000/catalogue/solid-fabrics-2_31/")
		self.driver.find_element_by_xpath("//select[@name='solid-fabrics-2']/option[text()='{0}']"
										  .format(self.options_two['fabric'])) \
			.click()
		time.sleep(.25)
		self.driver.find_element_by_xpath("//select[@name='bedswing-size']/option[text()='{0}']"
										  .format(self.options_two['bedswing-size'])) \
			.click()
		time.sleep(.25)

		self.driver.find_element_by_xpath("//select[@name='solid-fabrics-2-piping']/option[text()='{0}']"
										  .format(self.options_two['piping'])) \
			.click()
		self.driver.find_element_by_class_name("btn-add-to-basket").click()

		time.sleep(.25)
		self.checkout(total="$5,051.00", user = self.user2)

	def test_add_basket_three(self):

		## Navigate to  Fabrics
		self.driver.get("http://localhost:8000/catalogue/com_30/")
		self.driver.find_element_by_xpath("//select[@name='piping-for-cushions-and-pillows']/option[text()='{0}']"
										  .format(self.options_three['piping'])) \
			.click()
		time.sleep(.25)
		self.driver.find_element_by_xpath("//select[@name='bedswing-size']/option[text()='{0}']"
										  .format(self.options_three['bedswing-size'])) \
			.click()
		time.sleep(.25)

		self.driver.find_element_by_id("id_fabric-name-number").send_keys(self.options_three['fabric'])
		self.driver.find_element_by_class_name("btn-add-to-basket").click()

		time.sleep(.25)
		self.checkout(total="$1,586.20", user = self.user2)

	def test_add_basket_four(self):

		## Navigate to  Fabrics
		self.driver.get("http://localhost:8000/catalogue/com_30/")
		self.driver.find_element_by_xpath("//select[@name='piping-for-cushions-and-pillows']/option[text()='{0}']"
										  .format(self.options_three['piping'])) \
			.click()
		time.sleep(.25)
		self.driver.find_element_by_xpath("//select[@name='bedswing-size']/option[text()='{0}']"
										  .format(self.options_three['bedswing-size'])) \
			.click()
		time.sleep(.25)

		self.driver.find_element_by_id("id_fabric-name-number").send_keys(self.options_three['fabric'])
		self.driver.find_element_by_class_name("btn-add-to-basket").click()

		time.sleep(.25)
		self.checkout(total="$1,456.46", user = self.user1)
if __name__ == '__main__':
    unittest.main()



