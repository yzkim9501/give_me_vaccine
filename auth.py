import urllib

import jwt
import datetime
import hashlib

import requests
from flask import Flask, render_template, jsonify, request, Blueprint
from datetime import datetime, timedelta

import db

SECRET_KEY = 'givemevaccine'
db = db.get_db()

bp = Blueprint("auth", __name__)


@bp.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@bp.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    longlong_receive = request.form['longlong_give']
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})
    s=60*15 #체크박스에 체크 안했으면 로그인 유지시간 15분
    if longlong_receive=='true': #로그인 유지시간 1주일
        s=60*60*24*7
    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=s)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@bp.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    roadaddress_receive = request.form['roadaddress_give']
    detailaddress_receive = request.form['detailaddress_give']
    postcode_receive = request.form['postcode_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    r = getGPS_coordinate_for_KAKAO(roadaddress_receive, "3256ac8b9c70043c654930940b5a91ce")
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
        "road_address": roadaddress_receive,  # 프로필 이름 기본값은 아이디
        "detail_address": detailaddress_receive,  # 프로필 이름 기본값은 아이디
        "postcode": postcode_receive,  # 프로필 이름 기본값은 아이디
        "x": r['documents'][0]['road_address']['x'],
        "y": r['documents'][0]['road_address']['y']
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@bp.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


def getGPS_coordinate_for_KAKAO(address, MYAPP_KEY):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)
    }
    address = address.encode("utf-8")

    p = urllib.parse.urlencode(
        {
            'query': address
        }
    )

    result = requests.get("https://dapi.kakao.com/v2/local/search/address.json", headers=headers, params=p)
    return result.json()
