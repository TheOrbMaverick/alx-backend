#!/usr/bin/env python3
"""
Basic Flask app with a single route and Babel for i18n.
"""

from flask import Flask, render_template, request
from flask_babel import Babel


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


@babel.localeselector
def get_locale():
    """
    Determine the best match with supported languages.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """
    Route for the home page.
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
