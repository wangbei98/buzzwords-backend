import json
import time
from flask import Flask,request,abort
from flask import jsonify,make_response
from flask_restful import Api,Resource,fields,marshal_with,marshal_with_field,reqparse
from models import Question,Answer
from extensions import db

class AnswerAPI(Resource):
	# 新建一个answer
	def post(self):
		parse = reqparse.RequestParser()
		parse.add_argument('qid',type=int)
		parse.add_argument('atype',type=int)
		parse.add_argument('meaning',type=str)
		parse.add_argument('fromWhat',type=str)
		parse.add_argument('example',type=str)
		args = parse.parse_args()
		qid = args.get('qid')
		atype = args.get('atype')
		meaning = args.get('meaning')
		fromWhat = args.get('fromWhat')
		example = args.get('fromWhat')
		

		try:
			answer = Answer(qid = qid,atype = atype,meaning = meaning,fromWhat = fromWhat,example = example,created_time = int(time.time()))
			db.session.add(answer)
			db.session.commit()
			response = make_response(jsonify(code=0,message='OK',data = {'answer':answer.to_json()}))
			return response
		except:
			print("{} answer add: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), qid))
			db.session.rollback()
			response = make_response(jsonify(code=21,message = 'answer add fail'))
			return response
		finally:
			db.session.close()
	# 获取某个答案
	def get(self):
		parse = reqparse.RequestParser()
		parse.add_argument('aid',type=int)
		args = parse.parse_args()
		aid = args.get('aid')
		try:
			answer = Answer.query.get(aid)
			response = make_response(jsonify(code=0,message='OK',data = {'answer':answer.to_json()}))
			return response
		except:
			print("{} answer get: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), aid))
			response = make_response(jsonify(code=22,message = 'answer get fail'))

class QuestionAndAnswerAPI(Resource):
	# 新建一个词条
	def post(self):
		parse = reqparse.RequestParser()
		parse.add_argument('word',type=str)
		parse.add_argument('atype',type=int)
		parse.add_argument('meaning',type=str)
		parse.add_argument('fromWhat',type=str)
		parse.add_argument('example',type=str)
		args = parse.parse_args()
		word = args.get('word')
		atype = args.get('atype')
		meaning = args.get('meaning')
		fromWhat = args.get('fromWhat')
		example = args.get('fromWhat')
		
		# 查找词条是否存在
		print('0')
		try:
			print('1')
			question = Question.query.filter_by(word = word).first()
			print('2')
			print(question.to_json())
		except:
			print("{} question query failure: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), word))
		print('3')
		if not question:
			# 词条不存在
			# 新建question
			try:
				question = Question(word = word)
				db.session.add(question)
				db.session.commit()
			except:
				print("{} question add: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), word))
				db.session.rollback()

		print('4')
		qid = question.qid
		print(qid)
		try:
			print('5')
			answer = Answer(qid = qid,atype = atype,meaning = meaning,fromWhat = fromWhat,example = example,created_time = int(time.time()))
			print('6')
			db.session.add(answer)
			print('7')
			db.session.commit()
			print('8')
		except:
			print("{} answer add: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), qid))
			response = make_response(jsonify(code=21,message = 'answer add fail'))
			return response

		response = make_response(jsonify(code=0,message='OK',data = {'question':question.to_json()}))
		return response

