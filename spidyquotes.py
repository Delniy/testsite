#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run app
"""

import os
import json
import uuid
import random
import string
import base64
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from collections import Counter, defaultdict
from flask_limiter import Limiter
from flask import abort,request


app = Flask(__name__)


@app.before_request
def limit_remote_addr():
    if request.remote_addr != '194.165.23.3':
        abort(403)  # Forbidden

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/scroll")
def scroll():
    return render_template('ajax.html')


@app.route("/category/<cat>")
def category(cat=1):
    return render_template('category/'+cat+'.html')

@app.route("/article/<art>")
def article(art=1):
    return render_template('article/'+art+'.html')



if os.getenv('DYNO'):
    print('running in heroku, enabling limit of 1 request per second...')
    Limiter(app, global_limits=["10 per second"])
else:
    print('NOT running in heroku...')


if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--host')
    parser.add_argument('--throttle', action='store_true')
    args = parser.parse_args()
    if args.throttle:
        limiter = Limiter(app, global_limits=["1 per second"])
    app.run(debug=args.debug, host=args.host)
