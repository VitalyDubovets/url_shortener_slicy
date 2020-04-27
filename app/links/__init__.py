from flask import Blueprint


links = Blueprint('links', __name__)

from . import *

