# -*- coding: utf-8 -*-
import os
import sys
import json
HERE = os.path.dirname(os.path.realpath(__file__)) # add dependencies for AWS lambda to detect
sys.path.append(os.path.join(HERE, "libraries"))
from static_model import StaticModel

model = StaticModel()

def to_unicode(s):
	unicode(s,"utf-8") if isinstance(s,str) else s

def gateway_response(code, body):
	return {"statusCode": code, "body": json.dumps(body)}

def predict(event, context):
	try:
		payload = json.loads(event["body"])
		messages = payload["messages"]
	except Exception as e:
		return gateway_response(503,{"error":"The payload needs to be a valid JSON. Message: "+str(e)})


	try:
		for i,text in enumerate(messages):
			text = model.predict_email(text)
			text = model.predict_name(text)
			#text = model.predict_street(text)
			text = model.predict_number(text)
			messages[i] = text
		return gateway_response(200,{"messages":messages})
	except Exception as e:
		return gateway_response(503,{"error":"Prediction error. Message: "+str(e)})
