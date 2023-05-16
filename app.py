from flask import Flask, request
from redis import Redis
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import or_ as OR
from flask import jsonify
from flask import json
#--------------------------------------CONFIG---------------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test"
db = SQLAlchemy(app)
#-----------------------------------MODEL-------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    suggestion = db.Column(db.String(200), default = "No Text Here")
    def __repr__(self):
        return '<User %r>' % self.username
#----------------------------------------URL----------------------------
@app.route("/")
def up_service():
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    
    if root_url == developer_url:
        return "Succesfully Connected"
       
    return {"ok": "true"}
    

@app.route("/signup", methods = ['POST'])
def signup():
    data = request.get_json()
    if data.get("username", 0) != 0 and data.get("password", 0) != 0:
        users = User.query.all()
        print(users)
        username = []
        for user in users:
            username.append(user.username)
        if data["username"] not in username:
            try:
                user = User(
                username = data["username"],
                password = data["password"]
                )
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                return {"Database Error"}
        else:
            return {"false":"Username Exist"}
    else:
        return {"false":"Username or Password Required"}
    return {"ok":"User Create Successfuly"}


@app.route("/list", methods = ['GET'])
def list():
    users = User.query.all()
    print(users)
    username = []
    for user in users:
        username.append(user.username)
    return {"usernames":username}

@app.route("/login/<username>/<password>", methods = ["POST"])
def login(username, password):
    try:
        data = db.session.execute(User.query.filter_by(
                                    username=username,
                                    password=password)
                                    ).scalar_one()
        return {"ok":"true"}
    except Exception as e:
        return {"false":"invalid username or password"}

@app.route("/suggestion", methods = ['POST'])
def suggestion():
    data = request.get_json()
    if data.get("suggestion", 0) != 0 and data.get("username", 0) != 0 and data.get("password", 0) != 0:
        try:
            user = db.session.execute(User.query.filter_by(
                        username = data["username"],
                        password = data["password"])).scalar_one()
            user.suggestion = data["suggestion"]
            db.session.commit()
        except Exception as e:
                return {"false": "Database Error"}
        return {"ok" : "true"}
    else:
         return {"false" : "No Text Provideed or Username Password Empty"}


@app.route("/suggestionList", methods = ['GET'])
def suggestionList():
    users = User.query.all()
    print(users)
    username = []
    text = []
    result = {}
    for user in users:
        username.append(user.username)
        text.append(user.suggestion)
    for key in username:
        for value in text:
            result[key] = value
            text.remove(value)
            break
    return result

if __name__ == "__main__": 
    with app.app_context():
         db.create_all()
    app.run()
