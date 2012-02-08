#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import simplejson as json
import logging
import os

from os import path
from flask import Flask, render_template, Response

"""
Import lib
"""
sys.path.append(sys.path[0] + '/..')

from lib.motes import ListCommand, MotesInstaller, ContentCommand, PathCleaner, CommandLogger

"""
App
"""
motesite = Flask(__name__)
motesite.config.update(DEBUG=False, TESTING=False)

motes_path = ''

"""
Logger
"""
@motesite.before_request
def disable_web_logger():
  from werkzeug._internal import _logger

  _logger = logging.getLogger('werkzeug')
  _logger.disabled = True

"""
Routes + others
"""
@motesite.route('/')
def root():
  return render_template('index.html')

@motesite.route('/mote/<name>')
def get_mote(name=None):
  c = ContentCommand(motes_path, name)

  data = {'name': name, 'content': c.contents}

  return Response(json.dumps(data), mimetype='application/json')

@motesite.route('/motes')
def get_motes():
  lc = ListCommand(motes_path, False)
  files = []

  for file in lc.files():
    files.append(PathCleaner(file).short())

  return Response(json.dumps(files), mimetype='application/json')

@motesite.errorhandler(500)
def server_error(error):
  return render_template('500.html'), 500

"""
Runner
"""
def motes_web_start(path):
  global motes_path

  motes_path = path

  os.environ['WERKZEUG_RUN_MAIN'] = 'true'

  try:
    motesite.run(host='0.0.0.0', port=3000, debug=False, use_debugger=False)
  except KeyboardInterrupt:
    CommandLogger('Motes Web quit', True)

    pass

"""
Main
"""
if __name__ == '__main__':
  mi = MotesInstaller(path.abspath(path.dirname(__file__)) + '/../bin')

  motes_web_start(mi.path)
