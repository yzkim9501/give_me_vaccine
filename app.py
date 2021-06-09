import requests
from bs4 import BeautifulSoup

import db as db
import jwt
from flask import Flask, render_template, request, redirect, url_for

import auth, db
import maps
import detail

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = db.get_db()

SECRET_KEY = 'givemevaccine'


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get("https://kosis.kr/covid/covid_index.do", headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    occur = str(soup.select_one('#domesticDiv > div:nth-child(3) > ul > li:nth-child(1) > p.number').text)
    occur_before = \
        str(soup.select('#domesticDiv > div:nth-child(3) > ul > li:nth-child(1) > p.increase > span > span')).split(
            '>')[
            1].split('<')[0]

    fin = str(soup.select_one('#domesticDiv > div:nth-child(3) > ul > li:nth-child(2) > p.number').text)
    fin_before = \
        str(soup.select('#domesticDiv > div:nth-child(3) > ul > li:nth-child(2) > p.increase > span > span')).split(
            '>')[
            1].split('<')[0]

    ing = str(soup.select_one('#domesticDiv > div:nth-child(3) > ul > li:nth-child(3) > p.number').text)
    ing_before = \
        str(soup.select('#domesticDiv > div:nth-child(3) > ul > li:nth-child(3) > p.increase > span > span')).split(
            '>')[
            1].split('<')[0]

    dead = str(soup.select_one('#domesticDiv > div:nth-child(3) > ul > li:nth-child(4) > p.number').text)
    dead_before = \
        str(soup.select('#domesticDiv > div:nth-child(3) > ul > li:nth-child(4) > p.increase > span > span')).split(
            '>')[
            1].split('<')[0]

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info,
                               occur=f'{occur}({occur_before})', fin=f'{fin}({fin_before})',
                               ing=f'{ing}({ing_before})', dead=f'{dead}({dead_before})')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("auth.login", msg="로그인 정보가 존재하지 않습니다."))


if __name__ == '__main__':
    app.register_blueprint(auth.bp)
    app.register_blueprint(maps.bp)
    app.register_blueprint(detail.bp)
    app.run('0.0.0.0', port=5000, debug=True)
