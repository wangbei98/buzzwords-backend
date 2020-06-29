import json
import time
from flask import Flask,request,abort
from flask import jsonify,make_response
from flask_restful import Api,Resource,fields,marshal_with,marshal_with_field,reqparse
from models import Question,Answer
from extensions import db

class SearchAPI(Resource):
	def get(self):
		parse = reqparse.RequestParser()
		parse.add_argument('word',type=str)
		args = parse.parse_args()

		word = args.get('word')

		try:
			question = Question.query.filter_by(word = word).first()
			response = make_response(jsonify(code=0,message='OK',data = {'qid':question.qid}))
			return response
		except:
			response = make_response(jsonify(code=14,message='question search fail'))
			return response