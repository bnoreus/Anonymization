# -*- coding: utf-8 -*-
import re

class SentenceWrapper:
	def __init__(self,s):
		atoms = [s for s in re.split(u"([,\.\!\?:;\-\)\(\/\"\' ])",s) if s != ""]
		atoms = [Atom(s) for s in atoms]
		self.atoms = atoms

	def iter_words(self):
		for atom in self.atoms:
			if atom.is_word():
				yield atom

	def to_string(self):
		return u"".join([s.text for s in self.atoms])

	def iter(self):
		for atom in self.atoms:
			yield atom

class Atom:
	def __init__(self,text):
		self.text = text
		if re.search(u"([,\.\!\?:;\-\)\(\/\"\' ])",self.text) is None:
			self.type = "word"
		else:
			self.type = "punct"
	def is_word(self):
		return self.type == "word"
	def replace(self,new):
		self.text = new

def word_offsets(sentence):
	words = sentence.split(" ")
	offset = 0
	starts = []
	ends = []
	for w in words:
		if len(w) > 0:
			starts.append(offset)
			ends.append(offset+len(w))
		offset += len(w)+1

	return zip(starts,ends)

def word_offsets2(sentence):
	pass