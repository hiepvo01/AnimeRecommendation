from anime_flask import app
from anime_flask.routing.basic.constructors import *

@app.cli.command('db_create')
# Create database
def db_create():
    db.create_all()
    print("Database Created")

@app.cli.command('db_drop')
# Destroy database
def db_drop():
    db.drop_all()
    print('Database_dropped!')
    
@app.cli.command('db_seed')
# Sample database
def db_seed():
    mercury = Planet(planet_name="Mercury",
                     planet_type= 'Class D',
                     home_star = 'Sol',
                     mass = 3.258e23, 
                     radius= 1516,
                     distance = 35.98e6)
    venus = Planet(planet_name="Venus",
                     planet_type= 'Class K',
                     home_star = 'Sol',
                     mass = 4.8678e24, 
                     radius= 3760,
                     distance = 67.24e6)
    earth = Planet(planet_name="Earth",
                     planet_type= 'Class M',
                     home_star = 'Sol',
                     mass = 5.972e24, 
                     radius= 3959,
                     distance = 92.96e6)
    
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)
    
    test_user = User(username="William",
                     gender = "Male",
                     location="Chicago, Illinois",
                     email="test@test.com",
                     password="Bangfish")
    
    db.session.add(test_user)
    db.session.commit()
    print('Seed added')
    
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/trial')
def trial():
    return jsonify(message="trial")

@app.route('/not_found')
def not_found():
    return jsonify(message='That Resource was not found'), 404

@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message='Sorry ' + name + ", you are not old enough."), 401  
    else:
        return jsonify(message='Welcome ' + name + ", you are old enough."), 401
    return "hello"

# Variable Rule matching
@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message='Sorry ' + name + ", you are not old enough."), 401  
    else:
        return jsonify(message='Welcome ' + name + ", you are old enough."), 401
    return "hello"