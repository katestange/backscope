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
import numpy as np
import requests


from flaskr import db
from flaskr.nscope.models import *

bp = Blueprint("nscope", __name__)


# Creating a simple index route (this will error because we currently dont have an index.html"j
@bp.route("/index")
def index():
    return render_template("index.html")

# Sending simple json to the front end
@bp.route("/api/vuetest", methods=["GET"])
def vuetest():
    return jsonify({"Answer" : "This is a test", "Data" : [4.5123, 4.123, 9.123, 1.12309]})

@bp.route("/api/get_sequence/<id>/<num_elements>/<modulus>", methods=["GET"])
def get_sequence(id, num_elements, modulus):
    # get database entry
    seq = Sequence.get_seq_by_id(id)

    if seq == None:
        return "Error Invalid sequence: " + str(id)
    
    id = seq.id
    name = seq.name

    vals = np.array(seq.first_100_entries, dtype=np.int64)
    if int(modulus) != 0:
        vals = vals % int(modulus)

    if int(num_elements) < len(vals):
        vals = vals[0:int(num_elements)]


    # jsonify the data
    data = jsonify({'id': id, 'name': name, 'values': vals.tolist()})

    # return the data
    return data

@bp.route("/api/get_oeis_sequence/<oeis_id>/<num_elements>", methods=["GET"])
def get_oeis_seqence(oeis_id, num_elements):
   r = requests.get("https://oeis.org/{}/list".format(oeis_id))

   if r.status_code == 404:
       return "Error invalid OEIS ID: {}".format(oeis_id)

   seq_start_idx = r.text.find("<pre>") + 6 # consume up to the first array bracket
   seq_end_idx = r.text.find("</pre>") - 1 # consume back to the last array bracket
   sequence = r.text[seq_start_idx:seq_end_idx].replace('\n','').split(',')
   sequence = list(map(int,sequence))

   # Only concatenate the sequence if user requests less than what's available
   if len(sequence) > int(num_elements):
       sequence = sequence[:int(num_elements)]

   data = jsonify({'id': oeis_id, 'name': 'OEIS Sequence {}'.format(oeis_id), 'values': sequence})

   return data
