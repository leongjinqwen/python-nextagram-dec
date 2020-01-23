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

After connected to S3, create a function to upload the file directly to the respective bucket. 