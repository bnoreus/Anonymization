# -*- coding: utf-8 -*-
import re
import os
from sentence_utils import *
from train_utils import *
from name_deep_learning_model import NameDeepLearning

class StaticModel:
	def __init__(self):
		# Load static resources
		script_dir = os.path.dirname(__file__)

		self.first_names = set([unicode(line,"utf-8").strip().lower() for line in open(os.path.join(script_dir,"data/first_names.csv"))])
		self.last_names = set([unicode(line,"utf-8").strip().lower() for line in open(os.path.join(script_dir,"data/last_names.csv"))])
		self.streets = set([unicode(line,"utf-8").strip().lower() for line in open(os.path.join(script_dir,"data/streets.csv"))])

		self.deeplearning_model = NameDeepLearning()

	def predict_number(self,text):
		return re.sub(r"\d","<NUM>",text)

	def predict_email(self,text):
		return re.sub(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"," <EMAIL> ",text)
	
	def predict_name(self,text):
		wrapper = SentenceWrapper(text)
		for word in wrapper.iter_words():
			if word.text.lower() in self.first_names or word.text.lower() in self.last_names:
				word.replace("<NAME>")
		return wrapper.to_string()
	
	def predict_name_ann(self,text):
		wrapper = SentenceWrapper(text)
		before_batch = []
		after_batch = []
		for word in wrapper.iter_words():
			before_batch.append(pad_cut_string(wrapper.text_before(word),pad_right=False))
			after_batch.append(pad_cut_string(wrapper.text_after(word),pad_right=True))

		deeplearning_predictions = self.deeplearning_model.predict(before_batch,after_batch)
		for i,word in enumerate(wrapper.iter_words()):
			prediction = deeplearning_predictions[i]
			if prediction > 0.7:
				word.replace("<NAME>")
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