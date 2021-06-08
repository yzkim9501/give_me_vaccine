import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, Blueprint
from datetime import datetime, timedelta

import db

bp = Blueprint("testing", __name__)
db = db.get_db()


@bp.route('/maps')
def maps():
    msg = request.args.get("msg")
    return render_template('index.html', msg=msg)


@bp.route('/center', methods=["GET"])
def center():
    center_list = list(db.centers.find({}, {"_id": False}))
    return jsonify({"result": "success", "center_list": center_list})


@bp.route('/statistic', methods=["GET"])
def statistic():
    statistic_list = list(db.statistics.find({}, {"_id": False}))
    print(statistic_list)
    return jsonify({"result": "success", "statistic_list": statistic_list})
