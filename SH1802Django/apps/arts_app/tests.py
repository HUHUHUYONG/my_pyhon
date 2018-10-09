from django.test import TestCase

# Create your tests here.
from SH1802Django.settings import R


class A(object):
	def __init__(self, name, address):
		self.name = name
		self.address = address

	def __str__(self):
		return self.name

	def to_dict(self):
		return self.__dict__


if __name__ == "__main__":
	result = R.get("page:1:t:0")
	print(result)