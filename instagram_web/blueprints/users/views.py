from flask import Blueprint, render_template,request,redirect,url_for,flash
from models.user import User
from flask_login import current_user,login_required

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User(username=username,email=email,password=password)
    if user.save():
        flash("successfully create a new user",'info')
        return redirect(url_for('users.new'))
    else:
        for error in user.errors:
            flash(error,'danger')
        return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return render_template("users/show.html",username=username)
   


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    if current_user == user:
        return render_template("users/edit.html",user=user)
    else:
        flash("Unauthorized to edit.",'danger')
        return redirect(url_for('users.show',username=current_user.username))
        

@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)
    if current_user == user:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if username:
            user.username = username
            user.password = password
        if email:
            user.email = email
            user.password = password
        if password:
            user.password = password
        if user.save():
            flash('Successfully updated!','success')
            return redirect(url_for('users.edit',id=id))
        else:
            for error in user.errors:
                flash(error,'danger')
            return render_template("users/edit.html",user=user)
    else:
        flash("Unauthorized to edit.",'danger')
        return redirect(url_for('users.show',username=current_user.username))
        

