from datetime import datetime
import jwt
from flask import request, render_template, session, redirect, url_for
from app import app, generate_response, check_auth, check_token, db

from app.user.models import User
from app.event.models import Event, EventUser
from app.event.forms import EventForm


def get_user_id(username: str):
    query = db.select(User.id).where(User.username == username)
    user_id = db.session.execute(query).one_or_none()

    return user_id[0]


@app.route('/events/create', methods=['GET', 'POST'])
@check_auth
def event_create():
    username = session.get('username')
    form = EventForm()
    context = {}
    if form.validate_on_submit():
        event = Event()
        form.populate_obj(event)
        event.created_by = get_user_id(username)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('event_detail', id=event.id))
    return render_template('event/create.html', form=form, context=context, username=username)


@app.route('/events/<int:id>/update', methods=['GET', 'POST'])
@check_auth
def event_update(id: int):
    context = {}
    username = session.get('username')
    event = Event.query.get_or_404(id)
    event.set_date()
    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        return redirect(url_for('event_detail', id=event.id))
    return render_template('event/update.html', form=form, context=context, username=username)


@app.route('/events', methods=['GET'])
@check_auth
def events_list():
    username = session.get('username')
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 5, type=int)
    search_title = request.args.get('title')

    query = Event.query

    if search_title:
        query = query.filter(Event.title.ilike(f"%{search_title}%"))

    pagination = query.paginate(page=page, per_page=size, error_out=False)
    events = pagination.items

    user_id = get_user_id(username)

    return render_template(
        'event/list.html',
        events=events,
        username=username,
        user_id=user_id,
        pagination=pagination
    )


@app.route('/events/<int:id>', methods=['GET'])
@check_auth
def event_detail(id: int):
    username = session.get('username')
    event = db.get_or_404(Event, id)
    return render_template('event/detail.html', event=event, username=username)


@app.route('/events/<int:id>/users', methods=['GET', 'POST'])
@check_auth
def event_user_list(id: int):
    if request.method == 'GET':
        username = session.get('username')
        query = db.select(EventUser).where(EventUser.event_id == id)
        event_users = db.session.execute(query).scalars()
        return render_template('event/event_users.html', id=id, event_users=event_users, username=username)
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        event_user = EventUser(event_id=id, user_id=user_id, created_at=datetime.now().strftime("%Y-%m-%d"), score=0)
        db.session.add(event_user)
        db.session.commit()
        return redirect(url_for('events_list'))


@app.route('/api/events/', methods=['POST'])
@check_token
def add_event():
    data = {}
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 2, type=int)
    pagination = Event.query.paginate(page=page, per_page=size, error_out=False)
    for event in pagination.items:
        data[event.id] = event.to_dict()
    return generate_response(data, 201)


@app.route('/api/events/<int:id>/users', methods=['GET'])
@check_token
def api_event_user_list(id: int):
    event_users = EventUser.query.where(EventUser.event_id == id).all()
    data = {}
    for user in event_users:
        data[user.id] = user.to_dict()
    return generate_response(data, 201)


@app.route('/api/events/<int:id>/', methods=['PATCH'])
@check_token
def update_event(id: int):
    return generate_response(request.json)


@app.route('/api/events/<int:id>/', methods=['DELETE'])
@check_token
def delete_event(id: int):
    return generate_response(None, 204)


@app.route('/api/users/', methods=['GET'])
@check_token
def list_users():
    data = {}
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 2, type=int)
    pagination = User.query.paginate(page=page, per_page=size, error_out=False)
    for user in pagination.items:
        data[user.id] = user.to_dict()
    return generate_response(data)


@app.route('/api/users/', methods=['POST'])
@check_token
def add_user():
    return generate_response(request.json, 201)


@app.route('/api/users/<int:id>/', methods=['PATCH'])
@check_token
def update_user(id: int):
    return generate_response(request.json)


@app.route('/api/users/<int:id>/', methods=['DELETE'])
@check_token
def delete_user(id: int):
    return generate_response(None, 204)


@app.get('/api/login')
def api_login():
    data = request.get_json()

    username = data.get('username')
    expiration = datetime.datetime.now() + datetime.timedelta(hours=1)

    payload = {
        'username': username,
        'exp': expiration,
    }

    token = jwt.encode(payload, app.secret_key)

    token_info = {'token': token}

    return generate_response(token_info, 201)
