# -*- coding: utf-8 -*-
import unittest
from static_model import StaticModel
from sentence_utils import *

class StaticModelTest(unittest.TestCase):
	def test_name(self):
		model = StaticModel()
		#prediction = model.predict_name(u"hejsan david, mvh ( Henrik).")
		#self.assertEqual(prediction,u"hejsan <NAME>, mvh ( <NAME>).")
		print model.predict_name(u"Mitt namn är Kalle, men du kan kalla mig SAS.")
	def test_street(self):
		pass
		#model = StaticModel()
		#prediction = model.predict_street(u"jag bor   på vargungevägen. , nej")
		#self.assertEqual(prediction,u"jag bor   på <STREET>. , nej")
		
	def test_name_ann(self):
		pass
		#model = StaticModel()
		#text = u"Jag och min vän Kalle besökte er hemsida. "
		#prediction = model.predict_name_ann(text)
		
class SentenceUtilTest(unittest.TestCase):
	def test_sentence_wrapper(self):
		wrap = SentenceWrapper(u"hejsan! mamma, jag heter kalle!!")
		self.assertEqual(wrap.to_string(),u"hejsan! mamma, jag heter kalle!!")

if __name__ == "__main__":
	unittest.main()
