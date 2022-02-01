from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
api = Api(app)

#set the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init database
db=SQLAlchemy(app)

#init marshmallow
ma=Marshmallow(app)

#model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique =True)
    blog = db.Column(db.String(300))

    def __init__(self,name,blog):
        self.name = name
        self.blog = blog

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "name","blog")
        model = Post

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

if __name__ == "__main__":
    app.run(debug=True)

