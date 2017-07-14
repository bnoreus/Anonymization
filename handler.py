# -*- coding: utf-8 -*-
import os
import sys
import json
HERE = os.path.dirname(os.path.realpath(__file__)) # add dependencies for AWS lambda to detect
sys.path.append(os.path.join(HERE, "libraries"))
from static_model import StaticModel

model = StaticModel()

def gateway_response(code, body):
	return {"statusCode": code, "body": json.dumps(body)}


def predict(event, context):
	try:
		payload = json.loads(event["body"])
		text = unicode(payload["text"],"utf-8") if isinstance(payload["text"],str) else payload["text"]
	except Exception as e:
		return gateway_response(503,{"error":"The payload needs to be a valid JSON. Message: "+str(e)})


	try:
		text = model.predict_email(text)
		text = model.predict_name(text)
		text = model.predict_street(text)
		text = model.predict_number(text)
		text = text.encode("utf-8")
		return gateway_response(200,{"text":text})
	except Exception as e:
		return gateway_response(503,{"error":"Prediction error. Message: "+str(e)})
