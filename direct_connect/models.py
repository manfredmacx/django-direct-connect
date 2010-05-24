import binascii
from direct_connect import qaes
from django.db import models
from django.contrib.auth.models import User
from mmcd.custom.base.models import Customer, Transaction
from django.conf import settings

'''
See http://www.tylerlesmann.com/2008/dec/19/encrypting-database-data-django/
Written by Tyler Lesmann
and 
http://github.com/django-extensions/django-extensions/blob/master/django_extensions/db/fields/encrypted.py
The following is a hybrid of the two approaches because Lesmann's wasn't encrypting when the field value was set manually
instead of directly from a form
'''

class BaseEncryptedCharField(models.CharField):
	prefix = 'enc_str:::'
	def to_python(self, value):
		if value:
			if (value.startswith(self.prefix)):
				return qaes.decrypt(settings.AESKEY, binascii.a2b_base64(value[len(self.prefix):]))
			else:
				return value
		else:
			return ""
	def get_db_prep_value(self, value):
		if value:
			if not value.startswith(self.prefix):
				return self.prefix + binascii.b2a_base64(qaes.encrypt(settings.AESKEY, value))
			else:
				return value
		else:
			return ""
		
class EncryptedCharField(BaseEncryptedCharField):
	__metaclass__ = models.SubfieldBase


class Address:
	def __init__(self):
		self.delimiter = hex(31)
	def initialize(self, firstname, lastname, street, city, state, zipcode, country, countrycode, email_address=None, street2=None):
		self.firstname = firstname
		self.lastname = lastname
		self.street = street
		self.street2 = street2 or ""
		self.city = city
		self.state = state
		self.zipcode = zipcode
		self.country = country
		self.countrycode = countrycode
		self.email_address = email_address or ""
	def getAddressString(self):
		return self.delimiter.join((self.firstname, self.lastname, self.street, self.street2, self.city,
			self.state, self.zipcode, self.country, self.countrycode, self.email_address,))	
	def parseDecrypted(self, inStr):
		s = inStr.split(self.delimiter)
		self.initialize(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9])

class CreditCardInfo:
	def __init__(self, acct, expdate, cvv2, cctype):
		self.acct = acct
		self.expdate = expdate.strftime("%m%y")
		self.cvv2 = cvv2
		self.cctype = cctype

class Information(models.Model):
	address = EncryptedCharField(max_length=4000)
	transaction = models.ForeignKey(Transaction)
	user = models.ForeignKey(User, blank=True, null=True)
	customer = models.ForeignKey(Customer)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
class ServerResponse(models.Model):
	result = models.CharField(max_length=5)
	respMsg = models.CharField(max_length = 250)
	message = models.CharField(max_length = 250)
	authCode = models.CharField(max_length = 25, null = True)
	pnref = EncryptedCharField(max_length=10, null = True)
	hostCode = EncryptedCharField(max_length=10, null = True)
	getOrigResult = models.CharField(max_length=25, null = True)
	extData = models.CharField(max_length = 2000)
	ipAddress = models.IPAddressField()
	info = models.ForeignKey(Information, null=True)

