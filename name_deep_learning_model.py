# -*- coding: utf-8 -*-
import string


class NameDeepLearning:
	def __init__(self):
		CHARS = unicode(string.ascii_uppercase) + unicode(string.ascii_lowercase) + u" åäöÅÄÖ.-?!/:()\"\';_*%=+0123456789"
		CHARS = list(set(CHARS))+["<UNK>","<PAD>","<NAME>"]
		CHARS = {c:i for i,c in enumerate(CHARS)}
		self.CHARS = CHARS

	def predict(self,before_batch,after_batch):
		for i in range(len(before_batch)):
			before = [CHARS[char] if char in CHARS else CHARS["<UNK>"] for char in before_batch[i]]
			after = [CHARS[char] if char in CHARS else CHARS["<UNK>"] for char in after_batch[i]]

			before_batch[i] = before
			after_batch[i] = after

		predictions = self.predict_tf(before_batch,after_batch)
		return predictions

	def predict_tf(self,before_batch,after_batch):
		return [0.0]*len(before_batch)