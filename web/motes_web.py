#! /usr/bin/env python
# -*- coding: utf-8 -*-

from motes import *

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
  return render_template('index.html')

@app.route('/mote/<name>')
def get_mote(name=None):
  return '{"name": "aap", "content": "# Title"}'

@app.route('/motes')
def get_motes():
  lc = ListCommand(self.path, False)
  files = lc.files()

  return json.dumps(files)

if __name__ == '__main__':
  app.run(host='0.0.0.0')
