from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from classification import cwClassification, loadModel
import json, os



app = Flask(__name__)
api = Api(app)

CORS(app)
path_to_graph = "../inference_graph/frozen_inference_graph.pb"
detection_graph = loadModel(path_to_graph)

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
	lat, lng = cwClassification(float(lng),float(lat), detection_graph)

	print(str(lat) + " " + str(lng))

	return str(lat) + '/' + str(lng)

if __name__ == '__main__':
	app.run(port=5000)
