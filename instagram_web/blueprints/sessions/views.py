from flask import Blueprint, render_template,request,redirect,url_for,flash
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user, login_required

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    user = User.get_or_none(User.username==username)
    if user :
        password = request.form.get('password')
        hashed_password = user.password
        result = check_password_hash(hashed_password, password)
        if result:
            login_user(user)
            flash("success login!",'primary')
            return redirect(url_for('users.show',username=user.username))
        else:
            flash("cannot login!",'danger')
            return render_template('sessions/new.html')
    else:
        flash("user not exist!",'danger')
        return render_template('users/new.html')
        
    
@sessions_blueprint.route('/delete')
@login_required
def destroy():
    logout_user()
    return redirect(url_for('sessions.new'))