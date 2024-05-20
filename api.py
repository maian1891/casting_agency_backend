from flask import Flask, request, jsonify, abort
from werkzeug.exceptions import HTTPException
import traceback
from flask_cors import CORS

from auth.auth import AuthError, requires_auth
from databases.models import Actor, Movie, setup_db

def create_app(db_uri="", test_config=None):
    app = Flask(__name__)
    if db_uri:
        setup_db(app, db_uri)
    else:
        setup_db(app)
    
    configure_cors(app)
    register_after_request(app)
    register_retrieve_actors_routes(app)
    register_edit_actors_routes(app)
    register_movies_routes(app)
    register_error_handlers(app)
    return app

def configure_cors(app):
    """
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
        
    CORS(app, resources={r"/*": {"origins": "*"}})

def register_after_request(app):
    """
    Use the after_request decorator to set Access-Control-Allow
    """
        
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
        )
        return response

def register_retrieve_actors_routes(app):
    # ROUTES
    '''
    @TODO implement endpoint
        GET /actors
            it should be a public endpoint
            it should contain only the actor.short() data representation
        returns status code 200 and json {"success": True, "actors": actors} where actor is the list of actors
            or appropriate status code indicating reason for failure
    '''


    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def retrieve_actors(payload):
        try:
            selection = Actor.query.order_by(Actor.id).all()

            return jsonify({
                'success': True,
                'data': [actor.short() for actor in selection],
            })
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @TODO implement endpoint
        GET /actor-detail
            it should require the 'get:actor-detail' permission
            it should contain the actor.long() data representation
        returns status code 200 and json {"success": True, "actors": actors} where actor is the list of actors
            or appropriate status code indicating reason for failure
    '''


    @app.route('/actor-detail/<id>',  methods=['GET'])
    @requires_auth('get:actor-detail/:id')
    def retrieve_actor_detail(payload, id):
        print('Retrieving')
        try:
            actor = Actor.query.filter_by(id=id).one_or_none()

            if actor is None:
                abort(404)

            return jsonify({
                'success': True,
                'data': actor.long(),
            })
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @TODO implement endpoint
        POST /actor
            it should create a new row in the actor table
            it should require the 'post:actor' permission
            it should contain the actor.long() data representation
        returns status code 200 and json {"success": True} where actor an array containing only the newly created actor
            or appropriate status code indicating reason for failure
    '''


def register_edit_actors_routes(app):
    @app.route('/actor', methods=['POST'])
    @requires_auth('post:actor')
    def create_new_row_in_actor(payload):
        try:
            body = request.get_json()

            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)

            if new_name is None or new_age is None or new_gender is None:
                abort(422)

            actor = Actor(
                name=new_name,
                age=new_age,
                gender=new_gender
            )

            actor.insert()

            return jsonify({
                'success': True,
            })
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @TODO implement endpoint
        PATCH /actor/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:actor' permission
            it should contain the actor.long() data representation
        returns status code 200 and json {"success": True} where actor an array containing only the updated actor
            or appropriate status code indicating reason for failure
    '''


    @app.route('/actor', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(payload):
        try:
            body = request.get_json()

            new_id = body.get('id', None)
            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)

            actor = Actor.query.filter_by(id=new_id).one_or_none()

            if actor is None:
                abort(404)

            if new_name:
                actor.name = new_name
            if new_age:
                actor.age = new_age
            if new_age:
                actor.gender = new_gender
                
            actor.update()

            return jsonify({
                'success': True,
            })
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @TODO implement endpoint
        DELETE /actor/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actor' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''


    @app.route('/actor/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)

def register_movies_routes(app):


    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def retrieve_movies(payload):
        try:
            selection = Movie.query.order_by(Movie.id).all()

            return jsonify({
                'success': True,
                'data': [movie.short() for movie in selection],
            })
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @TODO implement endpoint
        GET /movie-detail
            it should require the 'get:movie-detail' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True, "movies": movies} where movie is the list of movies
            or appropriate status code indicating reason for failure
    '''


    @app.route('/movie-detail/<id>',  methods=['GET'])
    @requires_auth('get:movie-detail/:id')
    def retrieve_movie_detail(payload, id):
        try:
            movie = Movie.query.filter_by(id=id).one_or_none()
            
            if movie is None:
                abort(404)
                
            return jsonify({
                'success': True,
                'data': movie.long(),
            })
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @TODO implement endpoint
        POST /movie
            it should create a new row in the movie table
            it should require the 'post:movie' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True} where actor an array containing only the newly created actor
            or appropriate status code indicating reason for failure
    '''


    @app.route('/movie', methods=['POST'])
    @requires_auth('post:movie')
    def create_new_row_in_movie(payload):
        try:
            body = request.get_json()

            new_title = body.get('title', None)
            new_release_date = body.get('releaseDate', None)

            if new_title is None or new_release_date is None:
                abort(422)

            movie = Movie(
                title=new_title,
                release_date=new_release_date,
            )

            movie.insert()

            return jsonify({
                'success': True,
            })
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @TODO implement endpoint
        PATCH /movie/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:movie' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True} where movie an array containing only the updated movie
            or appropriate status code indicating reason for failure
    '''


    @app.route('/movie', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload):
        try:
            body = request.get_json()

            new_id = body.get('id', None)
            new_title = body.get('title', None)
            new_release_date = body.get('releaseDate', None)

            movie = Movie.query.filter_by(id=new_id).one_or_none()

            if movie is None:
                abort(404)

            if new_title:
                movie.title = new_title
            if new_release_date:
                movie.release_date = new_release_date
                
            movie.update()

            return jsonify({
                'success': True,
            })
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @TODO implement endpoint
        DELETE /movie/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:movie' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''


    @app.route('/movie/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)

def register_error_handlers(app):
    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    '''
    @TODO implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''

    '''
    @TODO implement error handler for 404
        error handler should conform to general task above
    '''


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404


    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''


    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['code'],
        }), error.status_code