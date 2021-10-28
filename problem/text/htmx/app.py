
# Copyright 2021 John Hanley.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# The software is provided "AS IS", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. In no event shall
# the authors or copyright holders be liable for any claim, damages or
# other liability, whether in an action of contract, tort or otherwise,
# arising from, out of or in connection with the software or the use or
# other dealings in the software.
import logging

from flask import Flask, jsonify, request
from page import page_bottom, page_top

app = Flask(__name__)

logger = logging.getLogger(__name__)


def create_app(runner):
    # Start the app with:
    #   $ flask run
    runner.configure(bind='5000')
    return app


@app.route('/')
def index():
    return jsonify(dict(hello='world'))


@app.route('/demo')
def demo():
    return page_top + page_bottom


@app.route('/clicked', methods=['POST'])
def clicked():
    logger.info(f'got a {request.method} request')
    if request.method == 'POST':
        logger.info(request.form.get('data'))
    return '<p>Hello world!'
