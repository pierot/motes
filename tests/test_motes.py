#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_motes.py

Created by Pieter Michels
"""

from motes import * 

from nose.tools import *
from StringIO import StringIO

"""
Tests
"""

class TestMotes:
  def setUp(self):
    self.motes_dir = './motes_test_dir/'

    self.held, sys.stdout = sys.stdout, StringIO()

  def test_motes_instance(self):
    m = Motes(self.motes_dir, 'list', '')
    
    assert isinstance(m, Motes) == True

  @raises(TypeError)
  def test_motes_instance_exception(self):
    m = Motes()

  def test_motes_commands(self):
    assert type(Motes.commands()) == dict

  def test_motes_command_exec(self):
    m = Motes(self.motes_dir, 'list', '') 

    assert isinstance(m.exec_command(), Command) == True

  def test_motes_list(self):
    m = Motes(self.motes_dir, 'list', '') 

    assert sys.stdout.getvalue() == ""


"""
Exec self
"""
if __name__ == '__main__':
  import nose

  nose.main()
