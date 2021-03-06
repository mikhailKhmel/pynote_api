import jwt
from functools import wraps
from passlib.hash import sha256_crypt

from config import *
from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
cache = SimpleCache()

from models import *


def get_hashed_password(password):
    return sha256_crypt.hash(password)


def check_password(password_from_db, password_from_request):
    return sha256_crypt.verify(password_from_request, password_from_db)


def make_cache(token_value):
    cache.set('token', Whitelist.query.filter_by(token=token_value).first(), timeout=5 * 60)


def get_cache_value(key):
    return cache.get(key)


def check_datetime_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token_req = request.get_json()['token']
        token = get_cache_value('token')
        if token is None:
            token = Whitelist.query.filter_by(token=token_req).first_or_404()
        checked_date = (datetime.datetime.now() - token.created).days
        if checked_date >= 60:
            black_token = Blacklist(token.user_uuid, token.token)
            db.session.add(black_token)
            db.session.delete(token)
            db.session.commit()
            return jsonify(error='Token is invalid'), 403
        else:
            make_cache(token.token)
            return func(checked_token=token)

    return wrapper


@app.route('/api/auth/registration', methods=['POST'])
def registration():
    data = request.get_json()['new_user']
    checked_user = User.query.filter_by(username=data['username']).first()
    if not checked_user:
        new_user = User(uuid=uuid4(), username=data['username'],
                        password=get_hashed_password(data['password']))

        new_white_token = Whitelist(uuid_user=new_user.uuid,
                                    token=jwt.encode(data, str(Config.get_secret_key), algorithm='HS256').decode(
                                        'utf-8'))
        make_cache(new_white_token.token)
        res = jsonify(token=new_white_token.token)
        res.set_cookie('username', new_user.username)

        db.session.add(new_user)
        db.session.add(new_white_token)
        db.session.commit()

        return res, 201
    else:
        return jsonify(error='User already exists'), 403


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()['auth_user']
    username = request.cookies.get('username')
    if username:
        checked_user = User.query.filter_by(username=username).first()
    else:
        checked_user = User.query.filter_by(username=data['username']).first_or_404()

    if check_password(checked_user.password, data['password']):
        checked_token = Whitelist.query.filter_by(uuid_user=checked_user.uuid).first()
        if check_datetime_token(checked_token):
            res = jsonify(token=checked_token.token)
            res.set_cookie('username', checked_user.username)
            make_cache(checked_token.token)
            return res, 201
        else:
            new_token = Whitelist(uuid_user=checked_user.uuid,
                                  token=jwt.encode(data, str(Config.get_secret_key), algorithm='HS256').decode('utf-8'))
            db.session.add(new_token)
            db.session.commit()
            res = jsonify(token=new_token.token)
            res.set_cookie('username', checked_user.username)
            make_cache(new_token.token)
            return res, 201
    else:
        return jsonify(error='Password is invalid'), 403


@app.route('/api/notes/add', methods=['POST'])
@check_datetime_token
def post_note(checked_token):
    note = request.get_json()['note']
    db.session.add(Note(uuid_author=checked_token.uuid_user, heading=note['heading'], content=note['content']))
    db.session.commit()
    return jsonify(success=True), 201


@app.route('/api/notes/get', methods=['GET'])
@check_datetime_token
def get_notes(checked_token):
    notes_db = Note.query.filter_by(uuid_author=checked_token.uuid_user).all()
    notes = [{'id': note.id, 'heading': note.heading, 'content': note.content} for note in notes_db]
    return jsonify(notes=notes), 201


@app.route('/api/notes/change', methods=['PUT'])
@check_datetime_token
def put_note(checked_token):
    changed_note = request.get_json()['note']
    note_db = Note.query.filter_by(uuid_author=checked_token.uuid_user, id=changed_note['id']).first()
    note_db.heading = changed_note['heading']
    note_db.content = changed_note['content']
    db.session.commit()
    return jsonify(success=True), 201


@app.route('/api/notes/remove', methods=['DELETE'])
@check_datetime_token
def delete_note(checked_token):
    db.session.delete(
        Note.query.filter_by(uuid_author=checked_token.uuid_user, id=request.get_json()['id']).first_or_404())
    db.session.commit()
    return jsonify(success=True), 201


@app.route('/api/todos/add', methods=['POST'])
@check_datetime_token
def add_todos(checked_token):
    for new_todo in request.get_json()['todos']:
        new_todo_db = Todo(uuid_author=checked_token.uuid_user, content=new_todo['content'])
        db.session.add(new_todo_db)
    db.session.commit()
    return jsonify(success=True), 201


@app.route('/api/todos/get', methods=['GET'])
@check_datetime_token
def get_all_todos(checked_token):
    todos_from_db = Todo.query.filter_by(uuid_author=checked_token.uuid_user).all()
    todos_list = [{'id': todo.id, 'content': todo.content, 'status': todo.status} for todo in todos_from_db]
    return jsonify(todos=todos_list), 201


if __name__ == '__main__':
    app.run()
