from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Movie(db.Model, SerializerMixin):
    __tablename__='movie_table'
    
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    rating = db.Column(db.Integer)
    description = db.Column(db.String)

    credits = db.relationship("Credit", back_populates="movies")

    serialize_rules = ('-credits.movies',)

    @validates('rating')
    def validate_rating(self, key, value):
        if 1 <= value <= 10:
            return value
        else:
            raise ValueError("A rating must be an integer between 1 and 10.")
        

    @validates('genre')
    def validate_genre(self, key, value):
        genre_types = [ "Action", "Comedy", "Drama", "Horror", "Romance", "Thriller", "Science Fiction", "Fantasy", "Mystery", "Adventure", "Crime", "Family", "Animation", "Documentary", "War" ]
        if value in genre_types:
            return value
        else:
            raise ValueError("Not a valid genre type.")


class Actor(db.Model, SerializerMixin):
    __tablename__='actor_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    age = db.Column(db.Integer)

    credits = db.relationship("Credit", back_populates="actors")

    serialize_rules = ('-credits.actors',)

    @validates("name")
    def validate_name(self, key, value):
        if value:
            return value
        else:
            raise ValueError("Not a valid name.")
        
    @validates("age")
    def validate_age(self, key, value):
        if value > 10:
            return value
        else:
            raise ValueError("Not a valid age.")


#JOIN TABLE - Columns and relationships
class Credit(db.Model, SerializerMixin):
    __tablename__='credit_table'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String, nullable=False)

    movie_id = db.Column(db.Integer, db.ForeignKey('movie_table.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor_table.id'), nullable=False)

    movies = db.relationship("Movie", back_populates="credits")
    actors = db.relationship("Actor", back_populates="credits")

    serialize_rules = ('-movies.credits', 'actors.credits')

    @validates("role")
    def validate_role(self, key, value):
        role_types = ["Performer", "Director", "Producor", "Playwright", "Lighting Design", "Sound Design", "Set Design"]
        if value in role_types:
            return value
        else:
            raise ValueError("Not a valid role type.")