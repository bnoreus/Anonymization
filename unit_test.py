# -*- coding: utf-8 -*-
import unittest
from static_model import StaticModel


class StaticModelTest(unittest.TestCase):
	def test_first_name(self):
		model = StaticModel()
		prediction = model.predict_first_name(u"hejsan")
		self.assertEqual(prediction,u"hejsan")

	def test_first_name2(self):
		return None
		model = StaticModel()
		for i,message in enumerate(open("../sensitive.txt")):
			message = unicode(message.strip(),"utf-8")
			anonymized = model.predict_first_name(message)
			anonymized = model.predict_last_name(anonymized)
			print "### BEFORE ###"
			print message
			print "### AFTER ###"
			print anonymized
			print "\n"
			if i > 1000:
				break
	def test_first_name3(self):
		model = StaticModel()
		for i,message in enumerate(open("../sensitive.txt")):
			message = unicode(message.strip(),"utf-8")
			model.predict_street(message)

if __name__ == "__main__":
	unittest.main()
