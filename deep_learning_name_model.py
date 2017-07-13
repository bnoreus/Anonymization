# -*- coding: utf-8 -*-
import os
import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
from deep_learning_utils import build_network
from deep_learning_config import DL_CHARS
class NameDeepLearning:
	def __init__(self):
		self.before_placeholder,self.after_placeholder,self.sess,self.output_layer = build_network()

		script_dir = os.path.dirname(__file__)
		path = os.path.join(script_dir,"models/model.ckpt")
		tf.train.Saver().restore(self.sess,path)

	def predict(self,before_batch,after_batch):
		for i in range(len(before_batch)):
			before = [DL_CHARS[char] if char in DL_CHARS else DL_CHARS["<UNK>"] for char in before_batch[i]]
			after = [DL_CHARS[char] if char in DL_CHARS else DL_CHARS["<UNK>"] for char in after_batch[i]]

			before_batch[i] = before
			after_batch[i] = after

		predictions = self.predict_tf(before_batch,after_batch)
		return predictions

	def predict_tf(self,before_batch,after_batch):
		feed_dict = {self.before_placeholder:before_batch,self.after_placeholder:after_batch}
		return list(np.reshape(self.sess.run(self.output_layer,feed_dict),[-1]))