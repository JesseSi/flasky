from flask import Blueprint

apply_blueprint = Blueprint('apply', __name__)

from . import views
