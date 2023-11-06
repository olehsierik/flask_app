import jwt
from werkzeug.exceptions import NotFound, InternalServerError
from flask import Flask, make_response, jsonify, session, redirect, url_for, request
from flask_migrate import Migrate

from app.database import db


def generate_response(content=None, status_code=200):
    if isinstance(content, (dict, list)) or content == None:
        response = jsonify(content)
    else:
        response = make_response(content)

    response.status_code = status_code
    return response


def check_auth(func):
    def wrapper(*args, **kwargs):
        username = session.get('username')
        if username is None:
            return redirect(url_for('login'))
        else:
            return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def check_token(func):
    def wrapper(*args, **kwargs):

        user_list = ['admin', 'user', 'root']

        auth_header = request.headers.get('Authentication')

        if auth_header == None:
            return generate_response('Missing TOKEN', 401)

        auth_header_list = auth_header.split(' ')

        try:
            if auth_header_list[0] != 'JWT':
                return generate_response('Invalid token type', 401)

            token = auth_header_list[1]
        except IndexError:
            return generate_response('Header invalid format', 401)

        try:
            data = jwt.decode(token, app.secret_key, algorithms=['HS256'])
            username = data.get('username')
            if username not in ['admin', 'user', 'root']:
                return generate_response('Unauthorized access!', 401)
        except jwt.InvalidSignatureError:
            return generate_response('Token has expired!', 401)
        except jwt.InvalidKeyError:
            return generate_response('Invalid security key', 401)
        except jwt.DecodeError:
            return generate_response('Decode Error', 401)

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


app = Flask(__name__)

app.config.from_pyfile('config.py')
app.logger.setLevel('INFO')

db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

from app.event import views
from app.user import views
from app.main import views


@app.errorhandler(NotFound)
def custom_err_handler_404(err):
    return generate_response("<h1>Looks like you're lost</h1>")


@app.errorhandler(InternalServerError)
def custom_err_handler_500(err):
    return generate_response('<h1>My bad...</h1>')
