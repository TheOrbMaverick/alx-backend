#!/usr/bin/env python3
"""
Basic Flask app with user login emulation and Babel for i18n.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime


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
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """
    Determine the best match with supported timezones.
    """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except UnknownTimeZoneError:
            pass
    if g.user:
        user_timezone = g.user.get('timezone')
        if user_timezone:
            try:
                return pytz.timezone(user_timezone).zone
            except UnknownTimeZoneError:
                pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


def get_user():
    """
    Return a user dictionary or None if the ID
    cannot be found or if login_as was not passed.
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
    user_timezone = get_timezone()
    current_time = datetime.now(pytz.timezone(user_timezone))
    formatted_time = current_time.strftime('%c')
    return render_template('index.html', current_time=formatted_time)


if __name__ == '__main__':
    app.run(debug=True)
