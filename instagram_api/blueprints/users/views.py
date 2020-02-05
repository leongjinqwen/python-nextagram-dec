from flask import Blueprint,jsonify,request
from models.user import User
from playhouse.shortcuts import model_to_dict # to convert model object to dictionary
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
from werkzeug.security import check_password_hash

users_api_blueprint = Blueprint('users_api',
                             __name__)

@users_api_blueprint.route('/', methods=['GET'])
def index():
    # get all users
    users = User.select()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'profileImage' : user.profile_image_url,
    } for user in users])
    # example of return 
    '''
    [
        {
            "id": 1,
            "profile_image": "2020-01-29_212426.404132kuroko.jpg",
            "username": "kuroko"
        },
        {
            "id": 3,
            "profile_image": "blank-profile-picture.png",
            "username": "jessica"
        },
    ]
    '''

@users_api_blueprint.route('/<id>', methods=['GET'])
def show(id):
    # get specific user
    user = User.get_or_none(User.id==id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'profileImage' : user.profile_image_url,
    })
    # example of return 
    '''
    {
        "id": 1,
        "profile_image": "2020-01-29_212426.404132kuroko.jpg",
        "username": "kuroko"
    }
    '''

@users_api_blueprint.route('/', methods=['POST'])
def create():
    # create new user
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    new_user = User(username=username,email=email,password=password)

    if not new_user.save():
        responseObject = {
            'status': 'failed',
            'message': new_user.errors
        }
        return jsonify(responseObject), 400
    else:
        access_token = create_access_token(identity=new_user.id)
        responseObject = {
            'status': 'success',
            'message': 'Successfully created a user and signed in.',
            'auth_token': access_token,
            'user': {"id": int(new_user.id), "username": new_user.username, "profileImage": new_user.profile_image_url}
        }
        return jsonify(responseObject), 201
    # example of successful return
    '''
    {
        "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODA3OTEzMzksIm5iZiI6MTU4MDc5MTMzOSwianRpIjoiMzJiM2IwYzYtYzNkMS00MDI4LThhNmItNTZmZjg2M2IwN2UyIiwiZXhwIjoxNTgwNzkyMjM5LCJpZGVudGl0eSI6MTAsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.hM4FlC92rf9yXHW8o7_xhsToezCubzS11VvhmuV3dB0",
        "message": "Successfully created a user and signed in.",
        "status": "success",
        "user": {
            "id": 10,
            "profileImage": "http://nextagram-backend.s3.amazonaws.com/blank-profile-picture.png",
            "username": "Testing123"
        }
    }
    '''

@users_api_blueprint.route('/login', methods=['POST'])
def login():
    # login user
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.get_or_none(User.username==username)

    if not user:
        responseObject = {
            'status': 'failed',
            'message': "No user found."
        }
        return jsonify(responseObject), 400
    else:
        hashed_password = user.password
        result = check_password_hash(hashed_password, password)
        access_token = create_access_token(identity=user.id)
        responseObject = {
            'status': 'success',
            'message': 'Successfully signed in.',
            'auth_token': access_token,
            'user': {"id": int(user.id), "username": user.username, "profile_picture": user.profile_image_url}
        }
        return jsonify(responseObject), 201   
    # example of successful return 
    '''
    {
        "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODA4MDc1MDIsIm5iZiI6MTU4MDgwNzUwMiwianRpIjoiNmNlZmU1NzQtNTI2ZC00ZmIyLWJmZjAtMDcxNDhhY2E4Yjc4IiwiZXhwIjoxNTgwODA4NDAyLCJpZGVudGl0eSI6MTAsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.bIEwBwzLqGqao841JHcqHD8GOsC0tTiuAw0kHrCKdEw",
        "message": "Successfully signed in.",
        "status": "success",
        "user": {
            "id": 10,
            "profile_picture": "http://nextagram-backend.s3.amazonaws.com/blank-profile-picture.png",
            "username": "Testing123"
        }
    }
    '''

@users_api_blueprint.route('/check_name', methods=['GET'])
def checkname():
    username = request.args.get('username')
    if not username:
        responseObject = {
            'status': 'failed',
            'message': 'No username found'
        }
        return jsonify(responseObject), 400
    else:
        user = User.get_or_none(User.username==username)
        if not user:
            responseObject = {
                'exists': False,
                'valid': True
            }
            return jsonify(responseObject)
        else:
            responseObject = {
                'exists': True,
                'valid': False
            }
            return jsonify(responseObject)
    # example of output if username not exist
    '''
    {
        "exists": false,
        "valid": true
    }
    '''