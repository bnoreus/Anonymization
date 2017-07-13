# -*- coding: utf-8 -*-
import re
import os
from sentence_utils import *

class StaticModel:
	def __init__(self):
		# Load static resources
		script_dir = os.path.dirname(__file__)

		self.first_names = set([unicode(line,"utf-8").strip().lower() for line in open(os.path.join(script_dir,"data/first_names.csv"))])
		self.last_names = set([unicode(line,"utf-8").strip().lower() for line in open(os.path.join(script_dir,"data/last_names.csv"))])
		self.streets = set([unicode(line,"utf-8").strip().lower() for line in open(os.path.join(script_dir,"data/streets.csv"))])

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
		"""
		offset = 0
		edited_text = ""
		for start,end in word_offsets(text):
			word = text[start:end]
			wordparts = re.sub(r"([,\.\!\?:;\-\)\(\/\"\'])",r" \1 ",word).split(" ")
			for i,wp in enumerate(wordparts): # Manipulate
				if wp.lower() in self.first_names or wp.lower() in self.last_names:
					wordparts[i] = "<NAME>"

			word = "".join(wordparts)
			edited_text += " "*(start-offset)+word
			offset = end

		return edited_text
		"""

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