from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)
marsh = Marshmallow(app)
api = Api(app)


class Movie(database.Model):
	__tablename__ = 'movie'
	id = database.Column(database.Integer, primary_key=True)
	title = database.Column(database.String(60), nullable = False)
	description = database.Column(database.String(250))
	year = database.Column(database.Integer)
	rents = database.relationship("Rent", backref = 'movie')

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
			title = request.json['title'],
			description = request.json['description'],
			year = request.json['year']
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
		database.session.delete(movie)
		database.session.commit()

		return '', 204


class Client(database.Model):
	__tablename__ = 'client'
	id = database.Column(database.Integer, primary_key=True)
	name = database.Column(database.String(50), unique = True, nullable = False)
	address = database.Column(database.String(60), nullable = False)
	phone = database.Column(database.String(16))
	rents = database.relationship("Rent", backref = 'client')

class ClientSchema(marsh.Schema):
	class Meta:
		fields = ("id", "name", "address", "phone")

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)


class ClientsListOrAdd(Resource):
	def get(self):
		clients = Client.query.all()

		return clients_schema.dump(clients)

	def post(self):
		new_client = Client(
			name = request.json['name'],
			address = request.json['address'],
			phone = request.json['phone']
		)
		database.session.add(new_client)
		database.session.commit()

		return client_schema.dump(new_client)


class ClientAccess(Resource):
	def get(self, client_id):
		client = Client.query.get_or_404(client_id)

		return client_schema.dump(client)

	def put(self, client_id):
		client = Client.query.get_or_404(client_id)

		if 'name' in request.json:
			client.name = request.json['name']
		if 'address' in request.json:
			client.address = request.json['address']
		if 'phone' in request.json:
			client.phone = request.json['phone']

		database.session.commit()

		return client_schema.dump(client)

	def delete(self, client_id):
		client = Client.query.get_or_404(client_id)
		database.session.delete(client)
		database.session.commit()

		return '', 204


class Rent(database.Model):
	__tablename__ = 'rent'
	id = database.Column(database.Integer, primary_key=True)
	movie_id = database.Column(database.Integer, database.ForeignKey('movie.id'))
	client_id = database.Column(database.Integer, database.ForeignKey('client.id'))
	notes = database.Column(database.String(128))

class RentSchema(marsh.Schema):
	class Meta:
		fields = ("id", "movie_id", "client_id", "notes")

rent_schema = RentSchema()
rents_schema = RentSchema(many=True)


class RentListOrAdd(Resource):
	def get(self):
		rents = Rent.query.all()

		return rents_schema.dump(rents)

	def post(self):
		new_rent = Rent(
			movie_id = request.json['movie_id'],
			client_id = request.json['client_id'],
			notes = request.json['notes']
		)
		database.session.add(new_rent)
		database.session.commit()

		return rent_schema.dump(new_rent)


class RentAccess(Resource):
	def get(self, rent_id):
		rent = Rent.query.get_or_404(rent_id)

		return rent_schema.dump(rent)

	def put(self, rent_id):
		rent = Rent.query.get_or_404(rent_id)

		if 'movie_id' in request.json:
			rent.movie_id = request.json['movie_id']
		if 'client_id' in request.json:
			rent.client_id = request.json['client_id']
		if 'notes' in request.json:
			rent.notes = request.json['notes']

		database.session.commit()

		return rent_schema.dump(rent)

	def delete(self, rent_id):
		rent = Rent.query.get_or_404(rent_id)
		database.session.delete(rent)
		database.session.commit()

		return '', 204
		

api.add_resource(MoviesListOrAdd, '/movies')
api.add_resource(MovieAccess, '/movie/<int:movie_id>')
api.add_resource(ClientsListOrAdd, '/clients')
api.add_resource(ClientAccess, '/client/<int:client_id>')
api.add_resource(RentListOrAdd, '/rents')
api.add_resource(RentAccess, '/rent/<int:rent_id>')

if __name__ == '__main__':
    app.run(debug=True)
