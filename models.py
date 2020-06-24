from flask_sqlalchemy import SQLAlchemy
from extensions import db
from flask_restful import fields,marshal_with

class Question(db.Model):
	__tablename__ = 'Question'
	qid = db.Column(db.Integer,primary_key=True)
	word = db.Column(db.String(50),unique=True)

	answers = db.relationship('Answer')

	question_fields = {
		'qid': fields.Integer,
		'word': fields.String,
		'answers':fields.List(fields.Nested({
				'aid':fields.Integer,
				'atype':fields.Integer,
				'meaning':fields.String,
				'fromWhat':fields.String,
				'example':fields.String
			}))
	}

	@marshal_with(question_fields)
	def to_json(self):
		return self
class Answer(db.Model):
	__tablename__ = 'Answer'
	aid = db.Column(db.Integer,primary_key=True)
	atype = db.Column(db.Integer,default=0)
	meaning = db.Column(db.String(200))
	fromWhat = db.Column(db.String(500))
	example = db.Column(db.String(500))

	qid = db.Column(db.Integer,db.ForeignKey('Question.qid'))

	answer_fields = {
		'aid':fields.Integer,
		'atype':fields.Integer,
		'meaning':fields.String,
		'fromWhat':fields.String,
		'example':fields.String
	}

	@marshal_with(answer_fields)
	def to_json(self):
		return self