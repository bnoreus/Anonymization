# -*- coding: utf-8 -*-
import re
def pad_cut_string(txt,pad_right=True,pad_steps=50):
	tokens = set(["<NAME>","<EMAIL>","<PAD>","<NUM>","<STREET>"])
	txt = re.split(u"("+"|".join(tokens)+")",txt)
	txt = [list(s) if not s in tokens else [s] for s in txt]
	txt = reduce(list.__add__,txt)
	if pad_right:
		txt = txt[:pad_steps]
		txt = txt + (pad_steps-len(txt))*["<PAD>"]
	else:
		txt = txt[-pad_steps:]
		txt = (pad_steps-len(txt))*["<PAD>"] + txt
	return txt
