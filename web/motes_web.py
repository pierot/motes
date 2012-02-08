#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from os import path
from flask import Flask, render_template

"""
Import lib
"""
sys.path.append(sys.path[0] + '/..')

from lib.motes import ListCommand, MotesInstaller

"""
App
"""
app = Flask(__name__)
mi = MotesInstaller(path.abspath(path.dirname(__file__)) + '/../bin')

lc = ListCommand(mi.path, False)
files = lc.files()

print files

"""
Routes
"""
@app.route('/')
def root():
  return render_template('index.html')

@app.route('/mote/<name>')
def get_mote(name=None):
  return '{"name": "aap", "content": "# Title"}'

@app.route('/motes')
def get_motes():
  lc = ListCommand(mi.path, False)
  files = lc.files()
  #return json.dumps(files)

"""
Main
"""
if __name__ == '__main__':
  app.run(host='0.0.0.0')
