from flask.typing import ResponseReturnValue
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, session, redirect, url_for, abort
from flask.views import View

from app import app, generate_response, db
from app.event.views import events_list
from app.user.models import User
from app.event.models import Event


def get_password(username: str):
    query = db.select(User.password).where(User.username == username)
    user_id = db.session.execute(query).one_or_none()
    try:
        return user_id[0]
    except Exception:
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('main/login.html')
    elif request.method == 'POST':
        context = {}
        username = request.form.get('username')
        current_pass = get_password(username)
        if current_pass:
            if check_password_hash(current_pass, request.form.get('password')):
                session['username'] = username
                return redirect(url_for('events_list'))
            context.update({"error": "Wrong password"})
            return render_template('main/login.html', **context)
        else:
            context.update({"error": "User not found"})
            return render_template('main/login.html', **context)


@app.get('/logout')
def logout():
    if session.get('username'):
        del session['username']
    return redirect(url_for('login'))


class BaseListView(View):
    def __init__(self, model):
        self.model = model

    def dispatch_request(self) -> ResponseReturnValue:
        items = self.model.query.all()
        headers = [column.name for column in self.model.__table__.columns][:3]
        return render_template('class/list.html', items=items, title=f'{self.model.__name__} List', headers=headers)


app.add_url_rule(
    "/class/users",
    view_func=BaseListView.as_view("users-list", User)
)

app.add_url_rule(
    "/class/events",
    view_func=BaseListView.as_view("courses-list", Event)
)


class BaseDetailView(View):
    def __init__(self, model):
        self.model = model

    def dispatch_request(self, id: int) -> ResponseReturnValue:
        item = self.model.query.get(id)
        print(item)
        if item is None:
            abort(404)
        return render_template('class/detail.html', item=item)


app.add_url_rule(
    "/class/users/<int:id>",
    view_func=BaseDetailView.as_view("users-detail", User)
)

app.add_url_rule(
    "/class/events/<int:id>",
    view_func=BaseDetailView.as_view("courses-detail", Event)
)
