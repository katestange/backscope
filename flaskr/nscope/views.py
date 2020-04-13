"""
Views for nscope model
"""

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import url_for
from flask import Flask, request, jsonify, render_template, send_file
from flask_login import LoginManager, current_user, login_user
from werkzeug.exceptions import abort
from sqlalchemy import or_, func
import pickle

from flaskr import db
from flaskr.nscope.models import *

bp = Blueprint("nscope", __name__)


# Creating a simple index route (this will error because we currently dont have an index.thml"j
@bp.route("/index")
def index():
    return render_template("index.html")

# Sending simple json to the front end
@bp.route("/vuetest", methods=["GET"])
def vuetest():
    return jsonify({"Answer" : "This is a test", "Data" : [4.5123, 4.123, 9.123, 1.12309]})

@bp.route("/get_sequence/<id>/<length>", methods=["GET"])
def get_sequence(id, length):
    # get database entry
    seq = Sequence.get_seq_by_id(id)
    id = seq.id
    name = seq.name
    print(id, name)
    func = pickle.loads(seq.code)
    length = int(length)

    vals = func(length)
    print(vals)


    # jsonify the data
    data = jsonify({'id': id, 'name': name, 'values': vals})

    # return the data
    return data

def luc(x):
    '''
    def help(x):
        if x == 0:
            return 1
        elif x == 1:
            return 2
        else:
            return luc(x-1) + luc(x-2)
    result = []
    for i in range(0, x+1):
        result.append(help(i))
    return result
    '''
    result = []
    for i in range(0, x+1):
        result.append(i)
    return result


@bp.route("/add_seq")
def add_seq():

    try:
        code = pickle.dumps(luc)
    except Exception as e:
        print(e)

    new_seq = Sequence(
        id = 'A00002',
        name = 'Lucas Numbers',
        code = code
    )

    try:
        new_seq.save_to_db()
        return {}, 200
    except Exception as e:
        print(e)
        return {'message': 'Error, please try again'}, 500

