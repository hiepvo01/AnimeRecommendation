from anime_flask import app
from anime_flask.routing.basic.constructors import *

@app.route("/users", methods=['GET'])
def users():
    users_list = User.query.all()
    result = users_schema.dump(users_list) 
    return jsonify(result)

@app.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    test = User.query.filter_by(email=email).first()
    username = request.json['username']
    test1 = User.query.filter_by(username=username).first()
    if test or test1:
        return jsonify(message='That email or username already exists'), 409
    else:
        gender = request.json['gender']
        password = request.json['password']
        location = request.json['location']
        user = User(username=username, gender=gender, location=location, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully'), 201
    
@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']   
        password = request.form['password']
    test = User.query.filter_by(email=email, password=password).first()
    if test:
        user = user_schema.dump(test)
        access_token = create_access_token(identity=email)
        return jsonify(message='login succeeded', access_token = access_token, user = user)
    else:
        return jsonify(message="Bad Email or Password"), 401
    
@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email:str):
    user = User.query.filter_by(email = email).first()
    if user:
        msg = Message("Your Planetary API password is " + user.password,
                      sender="admin@planetary.api.com",
                      recipients = [email])
        mail.send(msg)
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message="That email doesn't exist"), 401