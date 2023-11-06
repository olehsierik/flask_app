from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, session, redirect, url_for

from app import app, generate_response, check_auth, db

from app.user.models import User
from app.user.forms import UserRegistrationForm

from app.event.views import events_list
from app.main.views import login


@app.route('/users', methods=['GET'])
@check_auth
def users():
    username = session.get('username')
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    pagination = User.query.paginate(page=page, per_page=size, error_out=False)
    users = pagination.items
    return render_template('user/list.html', username=username, users=users, pagination=pagination)



@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = UserRegistrationForm()
    context = {}
    if form.validate_on_submit():
        existing_user = db.session.execute(db.select(User).where(User.username == form.username.data)).one_or_none()
        if existing_user:
            context.update({"error": "User already exists."})
        elif form.password.data != form.repeat_password.data:
            context.update({"error": "Passwords do not match."})
        else:
            user = User()
            form.populate_obj(user)
            user.password = generate_password_hash(user.password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("user/register.html", form=form, context=context)
