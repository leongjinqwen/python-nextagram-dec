from flask import Blueprint,jsonify,request
from models.image import Image
from playhouse.shortcuts import model_to_dict # to convert model object to dictionary
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity,decode_token

images_api_blueprint = Blueprint('images_api',
                             __name__)

@images_api_blueprint.route('/', methods=['GET'])
def index():
    # get all images of each user
    images = Image.select()
    return jsonify([{
        'id': image.id,
        'url' : image.image_url,
    } for image in images])
    # example of return 
    '''
    [
        {
            "id": 1,
            "url": "http://nextagram-backend.s3.amazonaws.com/2020-01-29_213330.931109lastgame.jpg"
        },
        {
            "id": 2,
            "url": "http://nextagram-backend.s3.amazonaws.com/2020-01-29_224838.484908kuroko_photo.jpg"
        },
    ]
    '''

@images_api_blueprint.route('/<user_id>', methods=['GET'])
@jwt_required
def show(user_id):
    # get specific user's images
    images = Image.select().where(Image.user==user_id)
    return jsonify([{
        'id': image.id,
        'url' : image.image_url,
    } for image in images])

@images_api_blueprint.route('/', methods=['POST'])
@jwt_required
def create():
    # upload image
    user_id = get_jwt_identity()
    if user_id:
        user = User.get_or_none(id=user_id)
        if user:
            file = request.files['image']
            if file and allowed_file(file.filename):
                output = upload_file_to_s3(file,os.getenv("AWS_BUCKET_NAME"))
                if output==True:
                    Image(image_path=file.filename,user = user.id).save()
                    responseObject = {
                        'success': 'ok',
                        'message': 'Your photo successfully uploaded.'
                    }
                    return jsonify(responseObject)
                else:
                    responseObject = {
                        'status': 'failed',
                        'message': 'Upload failed'
                    }
            else:
                responseObject = {
                    'status': 'failed',
                    'message': 'No file found'
                }
        else:
            responseObject = {
                'status': 'failed',
                'message': 'Authentication failed'
            }
            return jsonify(responseObject), 401
    else:
        responseObject = {
            'status': 'failed',
            'message': 'No authorization header found'
        }
        return jsonify(responseObject), 401
    

