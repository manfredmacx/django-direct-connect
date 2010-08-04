from django import forms
from direct_connect.fields import *

class CheckoutForm(forms.Form):
	firstname = forms.CharField(255, label="First Name")
	lastname = forms.CharField(255, label="Last Name")
	street = forms.CharField(255, label="Street 1")
	street2 = forms.CharField(255, label="Street 2", required=False)
	city = forms.CharField(255, label="City")
	state = forms.CharField(255, label="State")
	countrycode = CountryField(label="Country", initial="US")
	zip = forms.CharField(32, label="Postal / Zip Code")	

	def getAddress(self):
		from direct_connect.models import Address
		addr = Address()
		addr.initialize(self.cleaned_data['firstname'], self.cleaned_data['lastname'], self.cleaned_data['street'],
			self.cleaned_data['city'], self.cleaned_data['state'],self.cleaned_data['zip'], "", 
			self.cleaned_data['countrycode'], None, self.cleaned_data['street2'])
		return addr
		
class CheckoutFormWithCard(CheckoutForm):
	email_address = forms.EmailField(required=False)
	acct = CreditCardField(label="Credit Card Number")
	expdate = CreditCardExpiryField(label="Expiration Date")
	cvv2 = CreditCardCVV2Field(label="Card Security Code")
	
	def getAddress(self):
		addr = super(CheckoutFormWithCard, self).getAddress()
		addr.email_address = self.cleaned_data['email_address']
		return addr
			
	def getCard(self):
		from direct_connect.models import CreditCardInfo
		cc = CreditCardInfo(self.cleaned_data['acct'],self.cleaned_data['expdate'],self.cleaned_data['cvv2'], "")
		return cc
