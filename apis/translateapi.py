import json
import time
from flask import Flask,request,abort
from flask import jsonify,make_response
from flask_restful import Api,Resource,fields,marshal_with,marshal_with_field,reqparse
from models import Question,Answer
from extensions import db
import re
import json

def replace_word(matched):
	word = matched.group('word').lower()
	after = word
	try:
		question = Question.query.filter_by(word = word).first()
	except:
		return '[' + after + ']'
	if not question:
		return '[' + after + ']'
	answers = question.answers
	if len(answers) == 0:
		return '[' + after + ']'
	after = answers[0].meaning
	max_like = answers[0].like
	for answer in answers:
		if answer.like > max_like:
			after = answer.meaning
			max_like = answer.like
	return '[' + after + ']'

	

class TranslateAPI(Resource):
	def get(self):
		parse = reqparse.RequestParser()
		parse.add_argument('before',type=str)
		args = parse.parse_args()

		before = args.get('before')

		after = re.sub('(?P<word>[a-zA-Z0-9]+)',replace_word,before)

		response = make_response(jsonify(code=0,message='OK',data = {'after':after}))
		return response