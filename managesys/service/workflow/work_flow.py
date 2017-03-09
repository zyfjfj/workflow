from managesys import app
from flask import Blueprint

work_flow = Blueprint('work_flow', __name__, url_prefix='/workflow')
@work_flow.route('/')
def index():
    return 'work flow!'