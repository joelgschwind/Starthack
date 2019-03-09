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
	videoName = request.form['videoName']
	# Classify video here ->
	print('resultFiles/' + videoName + 'Result.json')
	response = open('resultFiles/' + videoName + 'Result.json', 'r')
	return response.read().replace('\n', '')

if __name__ == '__main__':
	app.run(port=5000)
