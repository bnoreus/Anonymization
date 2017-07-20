# -*- coding: utf-8 -*-
import re
import os
from sentence_utils import *
from train_utils import *
#from deep_learning_name_model import NameDeepLearning
#from deep_learning_config import DL_CONFIG_PADDED_SIZE

class StaticModel:
	def __init__(self):
		# Load static resources
		self.script_dir = os.path.dirname(__file__)
		self.uncommon_names = self.word_set("data/uncommon_names_with_words.txt")
		self.common_names = self.word_set("data/common_names_with_words.txt")
		self.uncommon_lastnames = self.word_set("data/uncommon_lastnames_with_words.txt")
		self.common_lastnames = self.word_set("data/common_lastnames_with_words.txt")
		self.guaranteed_names = self.word_set("data/guaranteed_names.txt")
		self.guaranteed_lastnames = self.word_set("data/guaranteed_lastnames.txt")
		
		self.streets = set([unicode(line,"utf-8").strip().lower() 
			for line in open(os.path.join(self.script_dir,"data/streets.csv"))])
		#self.deeplearning_model = NameDeepLearning()
		
	def word_set(self,url):
		s = {}
		
		for line in open(os.path.join(self.script_dir,url)):
			line = unicode(line,"utf-8").strip().lower()
			if line[0:2] == "__":
				s[line[2:]] = False
			else:
				if line in s:
					s[line] = True and s[line]
				else:
					s[line] = True
		return set([k for k,v in s.iteritems() if v])


	def predict_number(self,text):
		return re.sub(r"\d","<NUM>",text)

	def predict_email(self,text):
		return re.sub(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"," <EMAIL> ",text)
	
	def predict_name(self,text):
		wrapper = SentenceWrapper(text)
		for word in wrapper.iter_words():
			w = word.text.lower()
			if w in self.guaranteed_names or w in self.guaranteed_lastnames:
				word.replace("<NAME>")
			elif (w in self.common_names or
				 w in self.uncommon_names or
				 w in self.common_lastnames or 
				 w in self.uncommon_lastnames) and word.is_capitalized():
				word.replace("<NAME>")
		return wrapper.to_string()
	
	def predict_name_ann(self,text):
		wrapper = SentenceWrapper(text)
		before_batch = []
		after_batch = []
		for word in wrapper.iter_words():
			before_batch.append(pad_cut_string(wrapper.text_before(word),pad_right=False,pad_steps=DL_CONFIG_PADDED_SIZE))
			after_batch.append(pad_cut_string(wrapper.text_after(word),pad_right=True,pad_steps=DL_CONFIG_PADDED_SIZE))
			#print "Before"
			#print pad_cut_string(wrapper.text_before(word),pad_right=False,pad_steps=DL_CONFIG_PADDED_SIZE)
			#print "After"
			#print pad_cut_string(wrapper.text_after(word),pad_right=True,pad_steps=DL_CONFIG_PADDED_SIZE)

		deeplearning_predictions = self.deeplearning_model.predict(before_batch,after_batch)
		for i,word in enumerate(wrapper.iter_words()):
			prediction = deeplearning_predictions[i]
			if prediction > 0.0:
				word.replace(word.text+"["+str("%.3f" % prediction)+"]")
		return wrapper.to_string()

	def predict_street(self,text):
		wrapper = SentenceWrapper(text)
		for i,_ in enumerate(wrapper.iter()):
			street_words = []
			for j,word in enumerate(wrapper.iter()):
				if j >= i:
					street_words.append(word)
					street_name = u"".join([w.text for w in street_words])
					if street_name.lower() in self.streets:
						for atom in street_words:
							atom.replace("<STREET>")
				if j-i > 12:
					break

		return wrapper.to_string()