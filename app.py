import sys
import os
from flask import Flask, render_template
from flask_restful import Api
from apis.testapi import TestAPI
from apis.questionapi import QuestionAPI,QuestionsAPI,QuestionsToBeAnsweredAPI
from apis.answerapi import AnswerAPI,QuestionAndAnswerAPI,LikeAPI,DislikeAPI
from apis.translateapi import TranslateAPI
from flask_cors import CORS
from models import Question,Answer
import click
from extensions import db
from settings import config


# SQLite URI compatiblec
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app = Flask(__name__)

app.config['SECRET_KEY'] = config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'buzzwords.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
        click.echo('Drop tables')
    db.create_all()
    click.echo('Initialized database.')


@app.route('/')
def index():
    return '<h1>index<h1>'


api = Api(app)
# 请求跨域
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


api.add_resource(TestAPI, '/api/test', endpoint='test')

api.add_resource(QuestionAPI,'/api/question', endpoint='question')
api.add_resource(QuestionsAPI,'/api/questions', endpoint='questions')
api.add_resource(QuestionsToBeAnsweredAPI,'/api/q2beA', endpoint='q2beA')

api.add_resource(AnswerAPI,'/api/answer', endpoint='answer')
api.add_resource(QuestionAndAnswerAPI,'/api/word', endpoint='word')
api.add_resource(LikeAPI,'/api/answer/like', endpoint='like')
api.add_resource(DislikeAPI,'/api/answer/dislike', endpoint='dislike')

api.add_resource(TranslateAPI,'/api/translate', endpoint='translate')


