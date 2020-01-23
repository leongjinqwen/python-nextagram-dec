# Upload files to AWS
Make sure you already have **S3 bucket, access key and secret key** before go through this notes.

## How to connect to AWS?
Boto3 allows Python developers to write software that makes use of services like Amazon S3 and Amazon EC2. 

### <u>Step 1: Install `boto3` with pip</u>
```
pip install boto3
```

### <u>Step 2: Configuration to connect to your S3 bucket</u>
Make sure you store your S3 bucket, access key and secret key in your `.env` file, so that it won't be uploaded to github.

```py
# in .env file

AWS_BUCKET_NAME=your_bucket_name
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_DOMAIN=http://your_bucket_name.s3.amazonaws.com/
```

### <u>Step 3: Display Form</u>
Show your form in your html:
```html
<form action="{{url_for('create')}}" method="POST" enctype="multipart/form-data">

    <label for="user_file">Upload Your File</label>
    <br>
    <input type="file" name="user_file">
    <br>
    <button type="submit">Upload</button>

</form>
```

### <u>Step 4: Make connection to AWS</u>
Create a `helpers.py` in your `util` folder. Then use boto3 to establish a connection to the S3 service. 
```py
# in util/helpers.py

import boto3, botocore

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
```
After connected to S3, create a function to upload the file directly to the respective bucket. We'll use `boto3.client.upload_fileobj` provided by `boto3`, and this method accepts `file` and a `bucket_name` as arguments. 

Files uploaded to a S3 bucket can be accessed via a public URL that usually looks like this:
```html
https://nextagram-backend.s3.amazonaws.com/nextagram.jpg
https://<bucket_name>.s3.amazonaws.com/<filename>.<extension>
```
So, instead of saving the complete URL to database, we save the filename in our database in case we going to change the AWS bucket name due to deployment. 

```py
# in util/helpers.py

import os
from werkzeug.utils import secure_filename

def upload_file_to_s3(file, acl="public-read"):
    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    

    # after upload file to s3 bucket, return filename of the uploaded file
    return file.filename
```

### <u>Step 5: Call upload function</u>
Now you have a function to upload to bucket, we will then import and call it in the `upload` route. Before uploading the file, we need to do some checkings to make sure the file submitted from the form is valid file format. 
```py
# views.py

from flask import render_template, request, redirect, url_for
from instagram_web.util.helpers import upload_file_to_s3

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def create():

    # check whether an input field with name 'user_file' exist
    if 'user_file' not in request.files:
        flash('No user_file key in request.files')
        return redirect(url_for('new'))

    # after confirm 'user_file' exist, get the file from input
    file = request.files['user_file']

    # check whether a file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('new'))

    # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_file(file.filename):
        output = upload_file_to_s3(file) 
        
        # if upload success,will return file name of uploaded file
        if output:
            # write your code here 
            # to save the file name in database

            flash("Success upload")
            return redirect(url_for('show'))

        # upload failed, redirect to upload page
        else:
            flash("Unable to upload, try again")
            return redirect(url_for('new'))
        
    # if file extension not allowed
    else:
        flash("File type not accepted,please try again.")
        return redirect(url_for('new'))

```
At last we save the filename return from `upload_file_to_s3` into the database. 
