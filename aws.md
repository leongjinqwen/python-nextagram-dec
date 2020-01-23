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
<form action="/" method="POST" enctype="multipart/form-data">

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

```py
# in util/helpers.py

def upload_file_to_s3(file, acl="public-read"):
    
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
    

    # after upload file to s3 bucket, return a URL of the uploaded file
    return f"http://{os.getenv('AWS_BUCKET_NAME')}.s3.amazonaws.com/{file.filename}"
```

### <u>Step 5: Call upload function</u>
Now you have a function to upload to bucket, then where should we call the function? 
```py
# views.py

from flask import Flask, render_template, request, redirect
from werkzeug.security import secure_filename


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["POST"])
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
        filename = secure_filename(file.filename)
        output = upload_file_to_s3(file) 
        return str(output) # return the uploaded file URL

    # if file extension not allowed
    else:
        flash("File type not accepted,please try again.")
        return redirect(url_for('new'))

```