# -*- coding: utf-8 -*-
import tensorflow as tf
import tensorflow.contrib.slim as slim
from deep_learning_config import DL_CONFIG_PADDED_SIZE
from deep_learning_config import DL_CHARS
def build_network():
	sess = tf.Session()
	before_placeholder = tf.placeholder(tf.int64,[None,DL_CONFIG_PADDED_SIZE],name="before_placeholder")
	after_placeholder = tf.placeholder(tf.int64,[None,DL_CONFIG_PADDED_SIZE],name="after_placeholder")
	word_embedding = tf.get_variable("emb",[len(DL_CHARS),16])

	with tf.variable_scope("before_word"):
		embedding_layer_before = tf.nn.embedding_lookup(word_embedding,before_placeholder)
		embedding_layer_before = tf.expand_dims(embedding_layer_before,1)
		print "embedding_layer_before",embedding_layer_before.get_shape()
		conv_before = slim.conv2d(embedding_layer_before,32,[1,3],stride=2,padding="SAME",activation_fn=tf.nn.relu)
		#print "conv",conv_before.get_shape()
		#conv_before = slim.conv2d(conv_before,64,[1,3],stride=2,padding="SAME",activation_fn=tf.nn.relu)
		print "conv",conv_before.get_shape()
		flat_before = slim.flatten(conv_before)
		print "flattish_before",flat_before.get_shape()

	with tf.variable_scope("after_word"):
		embedding_layer_after = tf.nn.embedding_lookup(word_embedding,after_placeholder)
		embedding_layer_after = tf.expand_dims(embedding_layer_after,1)
		print "embedding_layer_after",embedding_layer_after.get_shape()
		conv_after = slim.conv2d(embedding_layer_after,32,[1,3],stride=2,padding="SAME",activation_fn=tf.nn.relu)
		conv_after = slim.conv2d(conv_after,64,[1,3],stride=2,padding="SAME",activation_fn=tf.nn.relu)
		
		print "conv",conv_after.get_shape()
		flat_after = slim.flatten(conv_after)
		print "flattish_after",flat_after.get_shape()


	concat = tf.concat([flat_before,flat_after],1)
	print "Concat",concat.get_shape()
	#output_layer = tf.nn.sigmoid(slim.fully_connected(flattish_before,1,activation_fn=None)+slim.fully_connected(flattish_after,1,activation_fn=None))
	hidden1 = slim.fully_connected(concat,256,activation_fn=tf.nn.relu)
	hidden2 = slim.fully_connected(hidden1,128,activation_fn=tf.nn.relu)
	output_layer = tf.nn.sigmoid(slim.fully_connected(hidden1,1,activation_fn=None))
	print "output_layer",output_layer.get_shape()
	return before_placeholder,after_placeholder,sess,output_layer