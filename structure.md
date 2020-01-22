# Flask Blueprint
Documentation: https://flask.palletsprojects.com/en/1.0.x/blueprints/

A Blueprint object works similarly to a Flask application object, but it is not actually an application. Rather it is a blueprint of how to construct or extend an application.

## Defining a Blueprint 
```py
# instagram_web/blueprints/users/views.py

from flask import Blueprint

# Set up a blueprint
users_blueprint = Blueprint('users_bp',
                            __name__,
                            template_folder='templates')
```

## Creating Routes Inside a Blueprint
```py
# instagram_web/blueprints/users/views.py

@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')
```

## Registering a Blueprint 
```py
# instagram_web/__init__.py

from app import app # import Flask instance from app.py
from instagram_web.blueprints.users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix="/users")
# to access to the routes that registered in users_blueprint, you need to use eg. http://example.com/users/<route>
```


## Templates
The blueprint's template folder is added to the search path of templates but with a lower priority than the actual application’s template folder. Means templates that a blueprint provided can be easily overrided.  
To prevent this, you creating templates in this format `blueprints/users/templates/users/index.html`. The reason for the extra `users` folder is to avoid getting our template overridden by a template named `index.html` in the actual application template folder.

```
instagram_web/
    blueprints/
        users/
            templates/
                users/
                    new.html
            views.py

        other_blueprint/
            templates/
                other_blueprint/
                    new.html
            views.py

    templates/
        _layout.html
        home.html
        new.html
    __init__.py
```

## Building URLs
To link from one page to another you can use the `url_for()` function with the name of the blueprint and a dot (.)
```py
url_for( 'users_bp.index' )
```


