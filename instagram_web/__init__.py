from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.endorsement.views import endorsement_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(endorsement_blueprint, url_prefix="/endorsement")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    from models.image import Image
    from models.user import User
    users = User.select()
    images = Image.select().order_by(Image.created_at.desc())
    return render_template('home.html',images=images,users=users)
