import urllib2, urllib
from django.conf import settings

TEST_NUMBERS = {
	'Visa' : 4055016727870315,
	'MasterCard' : 5424000000000015,
	'American Express' : 370000000000002,
	'Discover/Novus' : 6011000000000012,
	'Diners/Carte Blanche' : 38949114834801,
	'JCB' : 3088000000000017,
	'JAL' : 180077062049705,
}

class DirectConnect:
	# Reporting Transaction Detail Web services
	'''Retrieves card transaction details for a merchant'''
	def getCardTrx():
		url = "https://localhost/admin/ws/trxdetail.asmx?op=GetCardTrx"
		pass
	'''Retrieves card transaction summary for a merchant'''
	def getCardTrxSummary():
		pass
	'''Retrieves check transaction details for a merchant'''
	def getCheckTrx():
		pass
	'''Returns the name of the card issuer; such as Visa, MasterCard, AMEX, etc.'''
	def getCardType():
		pass	
	'''Retrieves payment type transaction summary of the current open batch for a merchant'''
	def getOpenBatchSummary():
		pass
	#Transact Web Services
	'''Retrieves information from the web service'''
	def GetInfo():
		pass
	'''Processes check transactions for a merchant'''
	def ProcessCheck():
		pass
	'''Parse XML response into dict '''
	def parse_reponse(self, response):
		if settings.DEBUG:
			print response
		namespace = '{http://TPISoft.com/SmartPayments/}'
		from xml.etree import ElementTree as ET
		return dict((e.tag.replace(namespace, ''), e.text) for e in ET.fromstring(response))
		
	'''Save Direct Connect response to database '''
	def record_response(self, respdict, ipAddress):
		from direct_connect.models import ServerResponse
		sr = ServerResponse()
		sr.ipAddress = ipAddress
		sr.result = respdict.get("Result", "ERROR")
		sr.respMsg = respdict.get("RespMSG", "ERROR")
		sr.message = respdict.get("Message", "ERROR")
		sr.extData = respdict.get("ExtData", None)
		sr.authCode = respdict.get("AuthCode", None)
		sr.pnref = respdict.get("PNRef", None)
		sr.hostCode = respdict.get("HostCode", None)
		sr.getOrigResult = respdict.get("GetGetOrigResult", None)
		sr.save()
		return sr

	'''Processes credit card transactions for a merchant'''
	def ProcessCreditCard(self, address, ccinfo, amt):
		url = settings.DC_URL + "/ProcessCreditCard"
		ext={
			'City' : address.city,
			'BillToState' : address.state,
		}
		params={
			'userName' : settings.DC_USERNAME,
			'Password' : settings.DC_PASSWORD,
			'TransType' :"Sale",
			'CardNum' : ccinfo.acct,
			'ExpDate' : ccinfo.expdate,
			'NameOnCard' : "",
			'Amount' : amt,
			'Zip' : address.zipcode,
			'Street' : address.street,
			'CVNum' : ccinfo.cvv2,
			'ExtData' : self.dict_to_xml(ext),
			'MagData' : "",
			'InvNum' : "",
			'PNRef' : "",
		}
		params_string = urllib.urlencode(params)
		response = urllib2.urlopen(url, params_string).read()
		return self.parse_reponse(response)
		
	'''Processes debit card transactions for a merchant'''
	def ProcessDebitCard():
		pass
	'''Processes EBT card transactions for a merchant'''
	def ProcessEBTCard():
		pass
	'''Processes gift card transactions for a merchant'''
	def ProcessGiftCard():
		pass
	'''Sends a signature to apply to a receipt transaction'''
	def ProcessSignature():
		pass
	'''Process Loyalty card transactions to a merchant'''
	def ProcessLoyaltyCard():
		pass
	#Validate Web Services
	'''Returns (T/F) if the card is a known commercial card'''
	def IsCommercialCard():
		pass
	'''Validates the credit card by checking the card length based on the card type, performing a mod 10 checksum, and validating the expiration date'''
	def ValidCard():
		pass
	'''Validates the credit card length'''
	def ValidCardLength():
		pass
	'''Validates the expiration date of the credit card'''
	def VaildExpDate():
		pass
	'''Validates the credit card by performing a mod 10 checksum on the  card number; returns (T/F)'''
	def ValidMod10():
		pass
	'''This Web service operation returns the name of the card issuer'''
	def GetCardType():
		pass
	'''This web service allows for returning the debit network ID if the debit card number matches any of these network's bin ranges'''
	def GetNetworkID():
		pass
	#Recurring Billing Web Services
	'''Allows customer information to be programmatically stored through web services for recurring billing.'''
	def AddRecurringCreditCard():
		pass
	'''Allows check information to be programmatically stored through web services for recurring billing.'''
	def AddRecurringCheck():
		pass
	'''Allows for processing credit card transactions in recurring billing.'''
	def ProcessCreditCardRecurring():
		pass
	'''Allows for processing ACH /check transactions for recurring billing.'''
	def ProcessCheckRecurring():
		pass
	'''Allows for programmatic management of existing check information for recurring billing.'''
	def ManageCheckInfo():
		pass
	'''Allows for programmatic management of credit card information for customers specific to recurring billing.'''
	def ManageCreditCardInfo():
		pass
	'''Allows for managing exisiting contracts for updates and modifications.'''
	def ManageContract():
		pass
	'''Allows for management of existing customers in the recurring billing web service.'''
	def ManageCustomer():
		pass
	'''Allows for modification of next billing date for recurring billing contracts.'''
	def ManageContractAddDaysToNextBillDt():
		pass
	''' Convert dict to XML to send as ExtData'''
	def dict_to_xml(self, d):
		from xml.dom.minidom import getDOMImplementation
		impl = getDOMImplementation()
		newdoc = impl.createDocument(None, "ExtData", None)
		retval = ""
		for k,v in d.items():
			elK = newdoc.createElement(k)
			elV = newdoc.createTextNode(v)
			elK.appendChild(elV)
			retval += elK.toxml()
		return retval


