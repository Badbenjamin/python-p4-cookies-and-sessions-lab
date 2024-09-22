#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from sqlalchemy_serializer import SerializerMixin

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/test')
def test():
    print('testing')
    return {},200

@app.route('/clear')
def clear_session():
    session['page_views'] = 0 
    print(session)
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    article_list = []
    for article in articles:
        article_list.append(article.to_dict())
    return article_list, 200
    

@app.route('/articles/<int:id>')
def show_article(id):
    page_views = 0
    article = Article.query.filter(Article.id == id).first()
    session['page_views'] = session.get('page_views') + 1 or 0
    
    print(session)
    if session['page_views'] <= 3:
        return article.to_dict(), 200
    else:
        return {'message': 'Maximum pageview limit reached'}, 401

    
    

if __name__ == '__main__':
    app.run(port=5555)
