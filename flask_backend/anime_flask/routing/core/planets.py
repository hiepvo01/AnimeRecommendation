from anime_flask import app
from anime_flask.routing.basic.constructors import *

@app.route("/planets", methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result) 

@app.route('/planet_details/<int:planet_id>', methods=["GET"])
def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id = planet_id).first()
    if planet:
        result = planet_schema.dump(planet) 
        return jsonify(result)
    else:
        return jsonify(message="That planet does not exist"), 404
    
@app.route('/add_planet', methods=["POST"])
@jwt_required
def add_planet():
    planet_name = request.form["planet_name"]
    test = Planet.query.filter_by(planet_name = planet_name).first()
    if test:
        return jsonify(message="The planet with that name already exists"), 409
    else:
        planet_type = request.form["planet_type"]
        home_star = request.form["home_star"]
        mass = float(request.form["mass"])
        radius = float(request.form["radius"])
        distance = float(request.form["distance"])
        
        new_planet = Planet(planet_name = planet_name, planet_type=planet_type, home_star= home_star, mass = mass, radius = radius, distance = distance)
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message="You added planet " + str(planet_name)), 201
    
@app.route('/update_planet', methods=['PUT'])
@jwt_required
def update_planet():
    planet_id = int(request.form["planet_id"])
    planet = Planet.query.filter_by(planet_id = planet_id).first()
    if planet:
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.radius = float(request.form['radius'])
        planet.distance = float(request.form['distance'])
        db.session.commit()
        return jsonify(message = "You updated planet " + str(planet.planet_name)), 202
    else:
        return jsonify(message="There is no such planet in dataset"), 404
     
@app.route("/remove_planet/<int:planet_id>", methods=["DELETE"])
@jwt_required
def remove_planet(planet_id:int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message="You deleted planet " + str(planet.planet_name)), 202
    else:
        return jsonify(message="That planet does not exist for delete"), 404
