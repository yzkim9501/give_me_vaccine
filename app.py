import jwt
from flask import Flask, render_template, request, redirect, url_for

import auth

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


SECRET_KEY = 'givemevaccine'

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("auth.login", msg="로그인 정보가 존재하지 않습니다."))


app.register_blueprint(auth.bp)

app.run('0.0.0.0', port=5000, debug=True)