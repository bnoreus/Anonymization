# -*- coding: utf-8 -*-

import json
from static_model import StaticModel
def lambda_gateway_response(code, body):
	return {"statusCode": code, "body": json.dumps(body)}

def predict(event, context):
	try:
		payload = json.loads(event["body"])
		return lambda_gateway_response(200,{"status":"OK","numRows":len(names)})
	except Exception as e:
		return lambda_gateway_response(503,{"error":str(e)})