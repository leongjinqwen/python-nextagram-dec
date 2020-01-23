from flask import Blueprint, render_template,request,redirect,url_for,flash
from models.user import User
from flask_login import current_user,login_required
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename

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
        

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@users_blueprint.route('/upload', methods=['POST'])
def upload():
    
    # check whether an input field with name 'user_file' exist
    if 'user_file' not in request.files:
        flash('No user_file key in request.files')
        return redirect(url_for('users.edit',id=current_user.id))

    # after confirm 'user_file' exist, get the file from input
    file = request.files['user_file']

    # check whether a file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('users.edit',id=current_user.id))

    # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        output = upload_file_to_s3(file) 
        if output:
            User.update(profile_image=output).where(User.id==current_user.id).execute()
            flash("Image successfully uploaded","success")
            return redirect(url_for('users.show',username=current_user.username))
        else:
            flash("Image upload failed","danger")
            return redirect(url_for('users.edit',id=current_user.id))

    # if file extension not allowed
    else:
        flash("File type not accepted,please try again.")
        return redirect(url_for('users.edit',id=current_user.id))