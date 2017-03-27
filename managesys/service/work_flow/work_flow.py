from flask import request
from managesys import db
from flask import Blueprint

from managesys.moudel.util import ok,objs_to_json
from models import FlowInfo
work_flow = Blueprint('work_flow', __name__, url_prefix='/workflow')


@work_flow.route('/')
def index():
    return 'work flow!'

@work_flow.route('/flowInfos',methods=['GET','POST'])
def flow_infos():
    query = db.session.query(FlowInfo)
    if request.method == "GET":
        flow_infos=query.all()
        if flow_infos:
            return ok(objs_to_json(flow_infos))