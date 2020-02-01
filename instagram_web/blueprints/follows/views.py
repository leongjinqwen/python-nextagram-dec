from flask import Blueprint, render_template,request,redirect,url_for,flash
from models.user import User
from models.fanidol import FanIdol
from flask_login import current_user, login_required
import os


follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')

@follows_blueprint.route('/<idol_id>')
@login_required
def create(idol_id):
    idol = User.get_by_id(idol_id)
    if current_user.follow(idol):
        flash(f"You follow {idol.username}","success")
        return redirect(url_for('users.show',username=idol.username))
    else:
        flash(f"You not yet follow {idol.username}","danger")
        return render_template('users/show.html',username=idol.username)

@follows_blueprint.route('/<idol_id>/delete')
@login_required
def destroy(idol_id):
    idol = User.get_by_id(idol_id)
    if current_user.unfollow(idol):
        flash(f"You unfollow {idol.username}","success")
        return redirect(url_for('users.show',username=idol.username))
    else:
        flash("Something went wrong, try again later.","danger")
        return render_template('users/show.html',username=idol.username)