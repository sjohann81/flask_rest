from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)
marsh = Marshmallow(app)
api = Api(app)


class Movie(database.Model):
	id = database.Column(database.Integer, primary_key=True)
	title = database.Column(database.String(60))
	description = database.Column(database.String(250))
	year = database.Column(database.Integer)

class MovieSchema(marsh.Schema):
	class Meta:
		fields = ("id", "title", "description", "year")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


class MoviesListOrAdd(Resource):
	def get(self):
		movies = Movie.query.all()

		return movies_schema.dump(movies)

	def post(self):
		new_movie = Movie(
			title=request.json['title'],
			description=request.json['description'],
			year=request.json['year']
		)
		database.session.add(new_movie)
		database.session.commit()

		return movie_schema.dump(new_movie)


class MovieAccess(Resource):
	def get(self, movie_id):
		movie = Movie.query.get_or_404(movie_id)

		return movie_schema.dump(movie)

	def put(self, movie_id):
		movie = Movie.query.get_or_404(movie_id)

		if 'title' in request.json:
			movie.title = request.json['title']
		if 'description' in request.json:
			movie.description = request.json['description']
		if 'year' in request.json:
			movie.year = request.json['year']

		database.session.commit()

		return movie_schema.dump(movie)

	def delete(self, movie_id):
		movie = Movie.query.get_or_404(movie_id)
		movie.delete()
		database.session.commit()

		return '', 204


api.add_resource(MoviesListOrAdd, '/movies')
api.add_resource(MovieAccess, '/movie/<int:movie_id>')


if __name__ == '__main__':
    app.run(debug=True)
