#!/usr/bin/env python3
"""
A basic Flask application demonstrating i18n (internationalization) support using Flask-Babel.

This app renders a homepage with translated content based on the user's locale preferences.
It supports both English and French languages.
"""

from flask import Flask, render_template, request
from flask_babel import Babel, _

class Config:
    """
    Configuration class for the Flask application.
    
    Attributes:
        LANGUAGES (list): Supported languages for the application.
        BABEL_DEFAULT_LOCALE (str): Default locale (language) for the app.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone for the app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

# Initialize Babel for internationalization
babel = Babel(app)

@babel.localeselector
def get_locale():
    """
    Select the best matching locale based on the 'Accept-Language' header sent by the user's browser.
    
    This function is automatically called by Flask-Babel to determine the appropriate language for
    the current request.

    Returns:
        str: The best matching language from the supported languages (Config.LANGUAGES).
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """
    Render the homepage with localized strings for the title and header.

    This route uses the Babel `gettext` function (aliased as `_`) to retrieve translated strings
    for the title ('home_title') and header ('home_header') of the page, based on the current locale.
    
    Returns:
        str: Rendered HTML content of the homepage.
    """
    return render_template(
        '3-index.html',
        home_title=_("home_title"),
        home_header=_("home_header")
    )

if __name__ == '__main__':
    app.run(debug=True)
    