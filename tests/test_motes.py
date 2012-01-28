#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_motes.py

Created by Pieter Michels
"""

from motes import * 
from nose.tools import *
from nose.plugins.capture import Capture

from StringIO import StringIO

"""
Tests
"""

motes_dir = './Motes/'
    
class TestMotes:
  #def setUp(self):
    #self.held, sys.stdout = sys.stdout, StringIO()

  #def tearDown(self):
    #sys.stdout = self.held

  def test_motes_instance(self):
    m = Motes(motes_dir, 'list', '')
    
    assert isinstance(m, Motes) == True

  @raises(TypeError)
  def test_motes_instance_exception(self):
    Motes()

  def test_motes_commands(self):
    assert type(Motes.commands()) == dict

  def test_motes_command_exec(self):
    m = Motes(motes_dir, 'list', '') 

    assert isinstance(m.exec_command(), Command) == True

class TestMotesCommands:
  def setUp(self):
    self.c = Capture()
    self.c.begin()

  def cap_end(self):
    self.c.end()

  def test_motes_list(self):
    m = Motes(motes_dir, 'list', '') 

    print self.c.buffer

    self.cap_end()

    print "test" + self.c.buffer


"""
Exec self
"""
if __name__ == '__main__':
  import nose

  nose.main()
