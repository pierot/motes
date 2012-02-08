#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import simplejson as json

from os import path
from flask import Flask, render_template

"""
Import lib
"""
sys.path.append(sys.path[0] + '/..')

from lib.motes import ListCommand, MotesInstaller, ContentCommand, PathCleaner

"""
App
"""
motesite = Flask(__name__)
mi = MotesInstaller(path.abspath(path.dirname(__file__)) + '/../bin')

"""
Routes
"""
@motesite.route('/')
def root():
  return render_template('index.html')

@motesite.route('/mote/<name>')
def get_mote(name=None):
  c = ContentCommand(mi.path, name)

  data = {'name': name, 'content': c.get_content()}

  return Response(json.dumps(data), mimetype='application/json')

@motesite.route('/motes')
def get_motes():
  lc = ListCommand(mi.path, False)
  files = []

  for file in lc.files():
    files.append(PathCleaner(file).short())

  return Response(json.dumps(files), mimetype='application/json')

@motesite.errorhandler(500)
def server_error(error):
  return render_template('500.html'), 500

"""
Main
"""
if __name__ == '__main__':
  motesite.run(host='0.0.0.0', port=3000)
