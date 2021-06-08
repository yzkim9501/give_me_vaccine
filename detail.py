from flask import Flask, render_template, Blueprint

import db

bp = Blueprint("detail", __name__)
db = db.get_db()

@bp.route('/detail/<id>')
def showDetail(id):
    center_info = db.centers.find_one({"id": int(id)})
    return render_template('detail.html', center_info=center_info)