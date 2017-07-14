from flask import Flask
from flask import request
from handler import predict

app = Flask(__name__)

@app.route("/predict",methods=["POST"])
def p():
	data = request.get_data(as_text=True)
	response = predict({"body":data},None) # Use like a lambda function
	return response["body"],response["statusCode"]

@app.route("/")
def hello():
	return "Use the /predict endpoint to anonymize data."

if __name__ == "__main__":
	app.run(debug=False,port=80)