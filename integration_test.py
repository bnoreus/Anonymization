# -*- coding: utf-8 -*-
from static_model import StaticModel

model = StaticModel()

for line in open("../sensitive.txt"):
	line = unicode(line,"utf-8").strip()
	text = line
	text = model.predict_email(text)
	text = model.predict_name(text)
	#text = model.predict_name_ann(text)
	text = model.predict_street(text)
	text = model.predict_number(text)
	if line != text:
		print line
		print ""
		print text
		print "\n=====\n"