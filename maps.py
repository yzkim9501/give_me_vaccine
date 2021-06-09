import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, Blueprint
from datetime import datetime, timedelta

import db

bp = Blueprint("testing", __name__)
db = db.get_db()


@bp.route('/maps', methods=["POST"])
def maps():
    username = request.form['username']
    user = db.users.find_one({"username": username})
    like_list = user.get("like")

    return jsonify({"like_list": like_list})


@bp.route('/center', methods=["GET"])
def center():
    # username = request.args.get("username")
    center_list = list(db.centers.find({}, {"_id": False}))
    return jsonify({"center_list": center_list})


@bp.route('/statistic', methods=["GET"])
def statistic():
    statistic_list = list(db.statistics.find({}, {"_id": False}))
    return jsonify({"statistic_list": statistic_list})


@bp.route('/center/like', methods=["POST"])
def center_like():
    id = request.form['id']
    username = request.form['username']
    print("Like:", id)
    print("username:", username)

    result = db.users.find_one({"$and": [{"username": username}, {"like": id}]})
    if result:
        db.users.update_one({'username': username}, {"$pull": {"like": id}})
    else:
        db.users.update_one({'username': username}, {"$push": {"like": id}})
    return jsonify({'result': 'success'})
