
import json
from flask import Flask,request,abort
from flask import jsonify,make_response
from flask_restful import Api,Resource,fields,marshal_with,marshal_with_field,reqparse

class TestAPI(Resource):
	def get(self):
		token = 'this is a test string from backend'
		response = make_response(jsonify(code=0,data={'token':token},message='OK'))
		return response

