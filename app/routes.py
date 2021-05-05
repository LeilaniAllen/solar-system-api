from app import db
from app.models.planet import Planet
from flask import request
from flask import request, Blueprint, make_response
from flask import jsonify

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("/<planet_id>", methods=["GET", "PUT","DELETE"], strict_slashes=False)
# this function get data from one planet and also updates data.
def handle_planet(planet_id):
    # Try to find the planet with the given id
    planet = Planet.query.get(planet_id)

    if planet is None:
        return jsonify("Not Found", 404), 404

    if request.method == "GET":
        return {
            "id": planet.id,
            "title": planet.title,
            "description": planet.description
        }

    elif request.method == "PUT":
        form_data = request.get_json()

        planet.title = form_data["title"]
        planet.description = form_data["description"]

        db.session.commit()
        return jsonify(f"Planet #{planet.id} successfully updated")

    elif request.method == "DELETE":
        db.session.delete(planet)
        db.session.commit()
        return jsonify(f"Planet #{planet.id} successfully deleted")


    


@planets_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def planet():
    if request.method == "GET":
        planet = Planet.query.all()
        planet_response = []
        for planet in planet:
            planet_response.append({
                "id": planet.id,
                "title": planet.title,
                "description": planet.description
            })
        return jsonify(planet_response), 200

    else:
        request_body = request.get_json() 
        new_planet = Planet(title = request_body["title"],
                            description = request_body["description"])

        db.session.add(new_planet)
        db.session.commit()

        return jsonify(f"Planet {new_planet.title} successfully created", 201)
