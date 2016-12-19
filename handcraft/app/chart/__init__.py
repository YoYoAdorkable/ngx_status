from flask import Blueprint

chart = Blueprint('chart', __name__)

from . import views
