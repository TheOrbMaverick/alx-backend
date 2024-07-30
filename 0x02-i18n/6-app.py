#!/usr/bin/env python3
"""
Basic Flask app with user login emulation and Babel for i18n.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _

class Config:
    """
    Configuration class for Flask app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

@babel.localeselector
def get_locale():
    """
    Determine the best match with supported languages.
    """
    # Check if the locale parameter is present in the URL
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    # Check if the user is logged in and has a preferred locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    # Fall back to the default behavior
    return request.accept_languages.best_match(app.config['LANGUAGES'])

def get_user():
    """
    Return a user dictionary or None if the ID cannot be found or if login_as was not passed.
    """
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None

@app.before_request
def before_request():
    """
    Function to be executed before all other functions.
    """
    g.user = get_user()

@app.route('/')
def index():
    """
    Route for the home page.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
