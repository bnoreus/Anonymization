# -*- coding: utf-8 -*-
from static_model import StaticModel

model = StaticModel()

for i,line in enumerate(open("../sensitive.txt")):
	line = unicode(line,"utf-8").strip()
	text = line
	#text = model.predict_email(text)
	text = model.predict_name(text)
	#text = model.predict_name_ann(text)
	#text = model.predict_street(text)
	#text = model.predict_number(text)
	if line != text:
		print "\n#### Before ####"
		print line
		print "\n#### After ####"
		print text
		print "\n=====\n\n"