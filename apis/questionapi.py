import json
import time
from flask import Flask,request,abort
from flask import jsonify,make_response
from flask_restful import Api,Resource,fields,marshal_with,marshal_with_field,reqparse
from models import Question
from extensions import db

class QuestionAPI(Resource):
	# 新建一个question
	def post(self):
		parse = reqparse.RequestParser()
		parse.add_argument('word',type=str)
		args = parse.parse_args()
		word = args.get('word')
		
		try:
			question = Question(word = word)
			db.session.add(question)
			db.session.commit()
			response = make_response(jsonify(code=0,message='OK',data = {'question':question.to_json()}))
			return response
		except:
			print("{} question add: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), word))
			db.session.rollback()
			response = make_response(jsonify(code=11,message = 'question add fail'))
			return response
		finally:
			db.session.close()
	# get一个question
	def get(self):
		parse = reqparse.RequestParser()
		parse.add_argument('qid',type=int)
		args = parse.parse_args()
		qid = args.get('qid')
		try:
			question = Question.query.get(qid)
			response = make_response(jsonify(code=0,message='OK',data = {'question':question.to_json()}))
			return response
		except:
			print("{} question get: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), qid))
			response = make_response(jsonify(code=12,message = 'question get fail'))
			return response
class QuestionsAPI(Resource):
	# get所有问题
	def get(self):
		try:
			questions = Question.query.all()
			response = make_response(jsonify(code=0,message='OK',data = {'questions':[question.to_json() for question in questions]}))
			return response
		except:
			print("{} question get_allfailure...".format(time.strftime("%Y-%m-%d %H:%M:%S")))
			response = make_response(jsonify(code=13,message = 'question get_all fail'))
			return response

class QuestionsToBeAnsweredAPI(Resource):
	# get所有问题
	def get(self):
		try:
			questions = Question.query.all()
			response = make_response(jsonify(code=0,message='OK',data = {'questions':[question.to_json() for question in questions if len(question.answers) == 0]}))
			return response
		except:
			print("{} question get_allfailure...".format(time.strftime("%Y-%m-%d %H:%M:%S")))
			response = make_response(jsonify(code=13,message = 'question get_all fail'))
			return response







