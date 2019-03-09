from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import json, os

app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route("/")
def hello():
	return "Welcome to the Crosswalk Recognition API"

@app.route('/classify', methods=['POST'])
def classify():
	""" 
	Receives classification requests and replies with the result 
	"""
	lat = request.form['lat']
	lng = request.form['lng']
	# Classify video here -> 

	return str(lat) + '/' + str(lng)

if __name__ == '__main__':
	app.run(port=5000)
