# -*- coding: utf-8 -*-
import re

class SentenceWrapper:
	def __init__(self,s):
		atoms = [s for s in re.split(u"([,\.\!\?:;\-\)\(\/\"\' ])",s) if s != ""]
		atoms = [Atom(s,i) for i,s in enumerate(atoms)]
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

	def text_before(self,atom):
		if atom.id != self.atoms[atom.id].id:
			raise Exception("The underlying array of atoms has been tampered with such that the ID's no longer make sense.")
		return u"".join([a.text for a in self.atoms[:atom.id]])

	def text_after(self,atom):
		if atom.id != self.atoms[atom.id].id:
			raise Exception("The underlying array of atoms has been tampered with such that the ID's no longer make sense.")
		return u"".join([a.text for a in self.atoms[atom.id+1:]])

class Atom:
	def __init__(self,text,id):
		self.text = text
		self.id = id
		if re.search(u"([,\.\!\?:;\-\)\(\/\"\' ])",self.text) is None:
			self.type = "word"
		else:
			self.type = "punct"
	def is_word(self):
		return self.type == "word"
	def replace(self,new):
		self.text = new
