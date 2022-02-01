from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

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

@app.route('/post', methods=['POST'])
def add_post():
    name = request.json['name']
    blog = request.json['blog']

    new_post = Post(name, blog)

    db.session.add(new_post)
    db.session.commit

    return post_schema.jsonify(new_post)

@app.route('/post', methods=['GET'])
def get_all_posts():
    all_posts = Post.query.all()
    result = Posts.schema.dump(all_posts)
    return jsonify(result.data)

@app.route('/post/<id>', methods=['GET'])
def get_product():
    post = Post.query.get(id)
    return post_schema.jsonify(post)

@app.route('/post/<id>', methods=['PUT'])
def update_post():
    post = Post.query.get(id):

    name = request.json['name']
    blog = request.json['blog']

    post.name = name
    post.blog = blog

    db.session.commit
    return post_schema .jsonify(post)

@app.route('/post/<id>', methods=['DELETE'])
def delete_post():
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return '', 204




if __name__ == "__main__":
    app.run(debug=True)

