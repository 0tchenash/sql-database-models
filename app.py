# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}
#Создаем неймспейсы
movies_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

#Схема для сериализации
class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

#Схема для сериализации
class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

#Схема для сериализации
class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


@movies_ns.route('/')
class MovieView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        movies = Movie.query

        if director_id:
            movies = movies.filter(Movie.director_id == director_id)
        if genre_id:
            movies = movies.filter(Movie.genre_id == genre_id)
        movies = movies.all()
        return MovieSchema(many=True).dump(movies), 200

    def post(self):
        data = request.get_json()
        new_movie = Movie(**data)
        db.session.add(new_movie)
        db.session.commit()
        db.session.close()
        return 'Размещение произведено успешно', 201


@movies_ns.route('/<int:mid>')
class MoviesView(Resource):
    def get(self, mid):
        if Movie.query.get(mid):
            movie = Movie.query.get(mid)
            return MovieSchema().dump(movie), 200
        else:
            return 'Данные не найдены', 404

    def put(self, mid):
        if Movie.query.get(mid):
            data = request.get_json()
            movie = Movie.query.get(mid)
            movie.id = data['id']
            movie.title = data['title']
            movie.description = data['description']
            movie.trailer = data['trailer']
            movie.year = data['year']
            movie.rating = data['rating']
            movie.genre_id = data['genre_id']
            movie.director_id = data['director_id']


            db.session.add(movie)
            db.session.commit()
            db.session.close()

            return 'Данные успешно изменены', 200
        else:
            return 'Данные не найдены', 404

    def delete(self, mid):
        if Movie.query.get(mid):
            movie = Movie.query.get(mid)

            db.session.delete(movie)
            db.session.commit()
            db.session.close()
            return 'Данные успешно удалены', 204
        else:
            return 'Данные не найдены', 404


@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        directors = Director.query.all()
        return DirectorSchema(many=True).dump(directors), 200

    def post(self):
        data = request.get_json()
        new_director = Director(**data)

        db.session.add(new_director)
        db.session.commit()
        db.session.close()

        return 'Данные добавлены успешно', 201

@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        if Director.query.get(did):
            director = Director.query.get(did)
            return DirectorSchema().dump(director), 200
        else:
            return 'Данные не найдены', 404

    def put(self, did):
        if Director.query.get(did):
            data = request.get_json()
            director = Director.query.get(did)
            director.id = data['id']
            director.name = data['name']

            db.session.add(director)
            db.session.commit()
            db.session.close()
            return 'Данные успешно обновлены', 201
        else:
            return 'Данные не найдены', 404

    def delete(self, did):
        if Director.query.get(did):
            data = Director.query.get(did)

            db.session.delete(data)
            db.session.commit()
            db.session.close()
            return 'Данные успешно удалены', 204
        else:
            return 'Данные не найдены', 404


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        genre = Genre.query.all()
        return GenreSchema(many=True).dump(genre), 200

    def post(self):
        data = request.get_json()
        new_genre = Genre(**data)

        db.session.add(new_genre)
        db.session.commit()
        db.session.close()

        return 'Данные добавлены успешно', 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        if Genre.query.get(gid):
            genre = Genre.query.get(gid)
            return GenreSchema().dump(genre), 200
        else:
            return 'Данные не найдены', 404

    def put(self, gid):
        if Genre.query.get(gid):
            data = request.get_json()
            genre = Genre.query.get(gid)
            genre.id = data['id']
            genre.name = data['name']

            db.session.add(genre)
            db.session.commit()
            db.session.close()
            return 'Данные успешно обновлены', 201
        else:
            return 'Данные не найдены', 404

    def delete(self, gid):
        if Genre.query.get(gid):
            data = Genre.query.get(gid)

            db.session.delete(data)
            db.session.commit()
            db.session.close()
            return 'Данные успешно удалены', 204
        else:
            return 'Данные не найдены', 404


if __name__ == '__main__':
    app.run(debug=True, port=5005)
