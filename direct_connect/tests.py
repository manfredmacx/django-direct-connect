from direct_connect.models import Address
from direct_connect.qaes import encrypt, decrypt
from django.conf import settings

def test1():
	a = Address()
	a.initialize("John", "Smith", "123 Fake Street", "Washington", "DC", "20009", 
		"US", "US", "jrenaut@localhost.com", "Apt 2")
	s = a.getAddressString()
	print s
	splt = s.split(a.delimiter)
	print splt
	b = Address()
	b.parseDecrypted(s)
	print b.firstname, b.street
	c = Address()
	c.initialize("John", "Smith", "123 Fake Street", "Washington", "DC", "20009", 
		"US", "US", "jrenaut@localhost.com")
	cs = c.getAddressString()
	print cs
	d = Address()
	d.parseDecrypted(cs)
	print d.firstname, d.state
	encS = encrypt(settings.AESKEY, s)
	print encS
	decS = decrypt(settings.AESKEY, encS)
	print decS
	e = Address()
	e.parseDecrypted(decS)
	print e.firstname, e.lastname, e.state
	
	
if __name__ == "__main__":
	test1()
