#!/usr/bin/env python3
"""
Basic Flask app with a single route and Babel for i18n.
"""

from flask import Flask, render_template, request
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
app.url_map.strict_slashes = False

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

    Uses the Babel `_` function to get translated strings for the title 
    and header based on the selected language.
    """
    return render_template(
        '3-index.html',
        home_title=_("home_title"),
        home_header=_("home_header")
        )


if __name__ == '__main__':
    app.run(debug=True)
