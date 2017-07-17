# -*- coding: utf-8 -*-
from __future__ import print_function
from csv import DictReader
import requests
from datetime import datetime
import re
import json
import argparse


parser = argparse.ArgumentParser(description='Anonymize some messages.')
parser.add_argument('url', type=str,help='a url to .csv file of messages')
args = parser.parse_args()

INPUT_URL = args.url
API_URL = "https://jb305p1y5i.execute-api.eu-west-1.amazonaws.com/dev/predict"

def iter_file(url):
	file = open(url)
	header = unicode(file.readline(),"utf-8").strip()
	if header != u"Timestamp,ConversationId,CustomerSpeaking,Message":
		raise Exception("Invalid/No header! Make sure your hear has the following format:\n\tTimestamp,ConversationId,CustomerSpeaking,Message")

	for line in file:
		line = unicode(line,"utf-8").strip().split(",")
		if len(line) < 4:
			raise Exception("Every row must have four columns (Timestamp, ConversationId, CustomerSpeaking and Message)")

		try:
			timestamp = datetime.strptime(line[0],"%Y-%m-%d %H:%M:%S")
		except Exception as e:
			raise Exception("Invalid timestamp. Format must be YYYY-MM-DD HH:MM:SS . Value was: "+str(line[0])+str(e))

		convo_id = line[1].lower()
		try:
			int(convo_id,16)
		except Exception as e:
			raise Exception("Convo ID must be number in the base ten or hexadecimal system")

		customer_speaking = line[2].lower()
		if customer_speaking != u"false" and customer_speaking != u"true":
			raise Exception("CustomerSpeaking must be true/false")

		message = u",".join(line[3:])

		yield timestamp,convo_id,customer_speaking,message

def predict(message_batch):
	r = requests.post(API_URL,data=json.dumps({"messages":message_batch}))
	if r.status_code != 200:
		raise Exception("Server replied with Non-OK status code "+str(r.status_code)+" Response: "+r.text)
	return r.json()["messages"]

if __name__ == "__main__":
	with open("output.csv","w") as f:
		f.write("Timestamp,ConversationId,CustomerSpeaking,Message\n")
		meta_batch = []
		message_batch = []
		for msg_idx,(timestamp,convo_id,customer_speaking,message) in enumerate(iter_file(INPUT_URL)):
			if msg_idx % 1000 == 0:
				print("{:,}".format(msg_idx))
			meta_batch.append(datetime.strftime(timestamp,"%Y-%m-%d %H:%M:%S")+","+convo_id+","+customer_speaking)
			message_batch.append(message)

			if len(message_batch) == 100:
				anonymized = predict(message_batch)
				for i,anon in enumerate(anonymized):
					f.write(meta_batch[i]+","+anon)
				meta_batch = []
				message_batch = []

		# Write any leftover rows
		anonymized = predict(message_batch)
		for i,anon in enumerate(anonymized):
			f.write(meta_batch[i].encode("utf-8")+","+anon.encode("utf-8")+"\n")
