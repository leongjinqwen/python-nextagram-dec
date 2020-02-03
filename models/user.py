from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import os
from playhouse.hybrid import hybrid_property

class User(UserMixin,BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    profile_image = pw.TextField(default="blank-profile-picture.png")
    private = pw.BooleanField(default=False)
    
    def follow(self,idol):
        from models.fanidol import FanIdol
        # check if has relationship in database
        if self.follow_status(idol)==None:
            return FanIdol(fan=self.id,idol=idol.id).save()
        else:
            return 0

    def unfollow(self,idol):
        from models.fanidol import FanIdol
        return FanIdol.delete().where(FanIdol.fan==self.id,FanIdol.idol==idol.id).execute()

    def approve_request(self,fan):
        from models.fanidol import FanIdol
        return FanIdol.update(approved=True).where(FanIdol.fan==fan.id,FanIdol.idol==self.id).execute()

    def follow_status(self,idol):
        from models.fanidol import FanIdol
        # check following status : 
        # if already follow => return that row, 
        # else return None(mean not follow this idol before)
        return FanIdol.get_or_none(FanIdol.fan==self.id,FanIdol.idol==idol.id)

    @hybrid_property
    def get_request(self):
        from models.fanidol import FanIdol
        return FanIdol.select().where(FanIdol.idol==self.id,FanIdol.approved==False)

    @hybrid_property
    def followers(self):
        from models.fanidol import FanIdol
        # to get all fans
        fans = FanIdol.select(FanIdol.fan).where(FanIdol.idol==self.id,FanIdol.approved==True)
        return User.select().where(User.id.in_(fans))

    @hybrid_property
    def followings(self):
        from models.fanidol import FanIdol
        # to get all idols
        idols = FanIdol.select(FanIdol.idol).where(FanIdol.fan==self.id,FanIdol.approved==True)
        return User.select().where(User.id.in_(idols))
    
    @hybrid_property
    def profile_image_url(self):
        return os.getenv("AWS_DOMAIN") + self.profile_image

    def validate(self):
        duplicate_username = User.get_or_none(User.username==self.username)
        duplicate_email = User.get_or_none(User.email==self.email)
        password_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

        # create new user
        if self.id == None:
            if duplicate_username:
                self.errors.append("Username not unique")
            if duplicate_email:
                self.errors.append("Email not unique")
            if re.search(password_regex, self.password) == None:
                self.errors.append("Minimum eight characters, at least one letter and one number")
            else :
                self.password = generate_password_hash(self.password)
        
        # update current user
        else:
            # handle change password
            if self.password != None :
                if re.search(password_regex, self.password) == None:
                    self.errors.append("Minimum eight characters, at least one letter and one number")
                else :
                    self.password = generate_password_hash(self.password)

            # handle change username or email
            else:
                if duplicate_username and duplicate_username.id != self.id :
                    self.errors.append("Username not unique")
                if duplicate_email and duplicate_email.id != self.id:
                    self.errors.append("Email not unique")
                else:
                    # save the original password
                    self.password = User.get_by_id(self.id).password
                
