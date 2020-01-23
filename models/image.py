from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images',on_delete="CASCADE")
    image_path = pw.TextField()
   

   