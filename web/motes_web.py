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
app = Flask(__name__)
mi = MotesInstaller(path.abspath(path.dirname(__file__)) + '/../bin')

"""
Routes
"""
@app.route('/')
def root():
  return render_template('index.html')

@app.route('/mote/<name>')
def get_mote(name=None):
  c = ContentCommand(mi.path, name)

  data = {}
  data['name'] = name
  data['content'] = c.get_content()

  return json.dumps(data)

@app.route('/motes')
def get_motes():
  lc = ListCommand(mi.path, False)
  files = []

  for file in lc.files():
    files.append(PathCleaner(file).short())

  return json.dumps(files)

"""
Main
"""
if __name__ == '__main__':
  app.run(host='0.0.0.0')
