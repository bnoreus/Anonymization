# -*- coding: utf-8 -*-
import re

class StaticModel:
	def __init__(self):
		# Load static resources
		self.first_names = set([line.strip().lower() for line in open("data/first_names.csv")])
		self.last_names = set([line.strip().lower() for line in open("data/last_names.csv")])
		self.streets = set([line.strip().lower() for line in open("data/streets.csv")])


	def predict_first_name(self,text):
		text = re.sub(r"([,\.\!\?:;\-\)\(\/\"\'])",r" \1 ",text)
		words = re.sub(u"[ ]+",u" ",text)
		words = words.split(" ")
		for i,word in enumerate(words):
			word = word.lower()
			if word in self.first_names:
				words[i] = "<FIRSTNAME>"
		return " ".join(words)


	def predict_last_name(self,text):
		text = re.sub(r"([,\.\!\?:;\-\)\(\/\"\'])",r" \1 ",text)
		words = re.sub(u"[ ]+",u" ",text)
		words = words.split(" ")
		for i,word in enumerate(words):
			word = word.lower()
			if word in self.first_names:
				words[i] = "<LASTNAME>"
		return " ".join(words)

	def predict_street(self,text):
		text = re.sub(r"([,\.\!\?:;\-\)\(\/\"\'])",r" \1 ",text)
		words = re.sub(u"[ ]+",u" ",text)
		words = words.split(" ")
		for i in range(len(words)):
			for j in range(i,min(i+12,len(words))):
				street = " ".join(words[i:j])
				if street in self.streets:
					print text
					print "Street: ",[street]
