#!/usr/bin/env python3

from models import db, Movie, Actor, Credit
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class Actors_Route(Resource):
    def get(self):
        all_actors = Actor.query.all()
        actor_dict = []
        for actor in all_actors:
            actor_dict.append(actor.to_dict(rules = ('-credits',)))
        return make_response(actor_dict, 200)
    def post(self):
        try:
            data = request.get_json()
            new_actor = Actor(
                name= data["name"],
                age= data["age"],
            )
            if new_actor:
                db.session.add(new_actor)
                db.session.commit()
                return make_response(new_actor.to_dict(), 201)
        except:
            return make_response({"errors": ["validation errors"]}, 400)

    
api.add_resource(Actors_Route, '/actors')

class Actor_By_ID(Resource):
    def get(self, id):
        single_actor = Actor.query.filter(Actor.id == id).first()
        if single_actor:
            return make_response(single_actor.to_dict(), 200)
        else:
            return({"error":"Actor not found"}, 404)
    def patch(self, id):
        single_actor = Actor.query.filter(Actor.id == id).first()
        if single_actor:
            try: 
                data = request.get_json()
                for attr in data:
                    setattr(single_actor, attr, data[attr])
                    db.session.add(single_actor)
                    db.session.commit()
                    return make_response(single_actor.to_dict(), 202)
            except:
                make_response({"errors": ["validation errors"]}, 400)
        else:
            return make_response({"error":"Actor not found"}, 404)
    def delete(self, id):
        single_actor = Actor.query.filter(Actor.id == id).first()
        if single_actor:
            db.session.delete(single_actor)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error":"Actor not found"}, 404)

api.add_resource(Actor_By_ID, '/actors/<int:id>')

class Movie_Route(Resource):
    def get(self):
        all_movies = Movie.query.all()
        movie_dict = []
        for movie in all_movies:
            movie_dict.append(movie.to_dict(rules = ('-credits',)))
        return make_response(movie_dict, 200)
    def post(self):
        try:
            data = request.get_json()
            new_movie = Movie(
                image= data["image"],
                title= data["title"],
                genre= data["genre"],
                rating= data["rating"],
                description= data["description"],
            )
            db.session.add(new_movie)
            db.session.commit()
            return make_response(new_movie.to_dict(), 200)
        except:
            return make_response({"errors": ["validation errors"]})

api.add_resource(Movie_Route, "/movies")

class Credits_Route(Resource):
    def get(self):
        all_credits = Credit.query.all()
        credit_dict = []
        for credit in all_credits:
            credit_dict.append(credit.to_dict(rules = ("-actors", "-movies")))
        return make_response(credit_dict, 200)
    def post(self):
        try:
            data = request.get_json()
            new_credit = Credit(
                actor_id = data["actor_id"],
                movie_id = data["movie_id"],
                role= data["role"]
            )
            db.session.add(new_credit)
            db.session.commit()
            return make_response(new_credit.to_dict(), 200)
        except:
            return make_response({"errors": ["validation errors"]})

api.add_resource(Credits_Route, "/credits")

class Credits_By_ID(Resource):
    def get(self, id):
        one_credit = Credit.query.filter(Credit.id == id).first()
        if one_credit:
            return make_response(one_credit.to_dict(), 200)
        else:
            return make_response({"error": "Credit not found"}, 404)
    def patch(self, id):
        one_credit = Credit.query.filter(Credit.id == id).first()
        if one_credit:
            try:
                data = request.get_json()
                for attr in data:
                    setattr(one_credit, attr, data[attr])
                db.session.add(one_credit)
                db.session.commit()
                return make_response(one_credit.to_dict(), 202)
            except:
                return make_response({"errors": ["validation errors"]}, 400)
        else:
            return make_response({"error": "Credit not found"}, 404)
    def delete(self, id):
        one_credit = Credit.query.filter(Credit.id == id).first()
        if one_credit:
            db.session.delete(one_credit)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"errors": "Credit not found"})

api.add_resource(Credits_By_ID, "/credits/<int:id>")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
