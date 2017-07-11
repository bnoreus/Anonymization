# -*- coding: utf-8 -*-
import re
from sentence_utils import word_offsets

class StaticModel:
	def __init__(self):
		# Load static resources
		self.first_names = set([unicode(line,"utf-8").strip().lower() for line in open("data/first_names.csv")])
		self.last_names = set([unicode(line,"utf-8").strip().lower() for line in open("data/last_names.csv")])
		self.streets = set([unicode(line,"utf-8").strip().lower() for line in open("data/streets.csv")])

	def predict_number(self,text):
		return re.sub(r"\d","<NUM>",text)

	def predict_email(self,text):
		return re.sub(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"," <EMAIL> ",text)
	
	def predict_name(self,text):
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

	def predict_street(self,text):
		step = 0
		offsets = word_offsets(text)
		while step < len(offsets):
			offsets = word_offsets(text)
			for i in range(1,12):
				# Slice the words into three parts
				processed = offsets[0:step]
				potential = offsets[step:step+i]
				remainder = offsets[step+i:len(offsets)]

				potential_streets = self.strip_street([text[start:end] for start,end in potential])

				if any([street.lower() in self.streets for street in potential_streets]):
					new_text = ""
					offset = 0
					# Turn what we already know into text
					for start,end in processed:
						new_text += " "*(start-offset)+text[start:end]
						offset = end
					# Anonymize street name
					new_text += " "*(potential[0][0]-offset)+"<STREET>"
					offset = potential[-1][1]

					# Add remainder
					for start,end in remainder:
						new_text += " "*(start-offset)+text[start:end]
						offset = end

					text = new_text
			step += 1
		return text

	def strip_street(self,text):
		potential_streets = []
		potential_streets.append(" ".join(text))
		
		tmp_text = text
		for i,w in enumerate(tmp_text):
			tmp_text[i] = re.sub(r"([,\.\!\?:;\-\)\(\/\"\']$)|(^[,\.\!\?:;\-\)\(\/\"\'])",r"",w)
		
		potential_streets.append(" ".join(tmp_text))

		tmp_text = text
		if len(tmp_text) == 1:
			splits = re.split(r"[,\.\!\?:;\-\)\(\/\"\']",tmp_text[0])
			potential_streets += splits
		else:
			tmp_text[0] = re.split(r"[,\.\!\?:;\-\)\(\/\"\']",tmp_text[0])[-1]
			tmp_text[-1] = re.split(r"[,\.\!\?:;\-\)\(\/\"\']",tmp_text[-1])[0]
			potential_streets.append(" ".join(tmp_text))

		return potential_streets