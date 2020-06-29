import json
import time
from flask import Flask,request,abort
from flask import jsonify,make_response
from flask_restful import Api,Resource,fields,marshal_with,marshal_with_field,reqparse
from models import Question,Answer
from extensions import db
import re

def replace_word(word):
	return 'hhh'

class TranslateAPI(Resource):
	def get(self):
		parse = reqparse.RequestParser()
		parse.add_argument('sentence',type=str)
		args = parse.parse_args()

		before = args.get('sentence')

		after = re.sub('(?P<word>[a-zA-Z0-9]+)',replace_word,before)

		response = make_response(jsonify(code=0,message='OK',data = {'after':after}))
		return response