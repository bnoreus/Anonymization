# -*- coding: utf-8 -*-
import unittest
from static_model import StaticModel
from sentence_utils import *

class StaticModelTest(unittest.TestCase):
	def test_name(self):
		model = StaticModel()
		prediction = model.predict_name(u"hejsan arvid, mvh ( henrik).")
		self.assertEqual(prediction,u"hejsan <NAME>, mvh ( <NAME>).")

	def test_street(self):
		model = StaticModel()
		prediction = model.predict_street(u"jag bor   på vargungevägen. , nej")
		self.assertEqual(prediction,u"jag bor   på <STREET>. , nej")
		
class SentenceUtilTest(unittest.TestCase):
	def test_word_offsets(self):
		sentence = u"hej jag  heter bure"
		o = word_offsets(sentence)
		self.assertEqual(len(o),4)
		self.assertEqual(o[0],(0,3))
		self.assertEqual(o[1],(4,7))
		self.assertEqual(o[2],(9,14))
		self.assertEqual(o[3],(15,19))

	def test_sentence_wrapper(self):
		wrap = SentenceWrapper(u"hejsan! mamma, jag heter kalle!!")
if __name__ == "__main__":
	unittest.main()
