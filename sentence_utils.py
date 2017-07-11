# -*- coding: utf-8 -*-

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