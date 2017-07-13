# -*- coding: utf-8 -*-
import re
def pad_cut_string(txt,pad_right=True,pad_steps=50):
	txt = re.split(u"(<NAME>|<PAD>)",txt)
	txt = [list(s) if (s != "<NAME>" and s != "<PAD>") else [s] for s in txt]
	txt = reduce(list.__add__,txt)
	if pad_right:
		txt = txt[:pad_steps]
		txt = txt + (pad_steps-len(txt))*["<PAD>"]
	else:
		txt = txt[-pad_steps:]
		txt = (pad_steps-len(txt))*["<PAD>"] + txt
	return txt
