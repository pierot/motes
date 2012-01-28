#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_motes.py

Created by Pieter Michels
"""

from os import path

from motes import * 
from nose.tools import *
from nose.plugins.capture import Capture

from StringIO import StringIO

"""
Tests
"""

cwd = path.abspath(path.dirname(__file__))
motes_dir = cwd + '/Motes/'

class TestMotes:
  def setUp(self):
    self.c = Capture()
    self.c.begin()

  def tearDown(self):
    self.c.end()

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


class TestMotesListCommand:
  def setUp(self):
    self.c = Capture()
    self.c.begin()

    self.c_begin = "\033[94m"
    self.c_end = "\033[0m\n"
    self.prefix = u'ە '.encode('utf-8')

  def cap_end(self):
    self.c.end()

  def test_motes_list(self):
    m = Motes(motes_dir, 'list', '') 

    self.cap_end()

    title = self.c_begin + self.prefix + "All motes\n" + self.c_end
    content = self.c_begin + "[0]\ttest" + self.c_end

    assert self.c.buffer == title + content


"""
def setup_ask_value_fixtures(testcase):
    testcase.mock_tracker = minimock.TraceTracker()
  
    testcase.test_response = str(object())
  
    minimock.mock(
        "__builtin__.raw_input",
        returns=testcase.test_response,
        tracker=testcase.mock_tracker)
    minimock.mock(
        "sys.stderr",
        tracker=testcase.mock_tracker)
"""

"""
class TestMotesOpenNonExistence:
  def setUp(self):
    setup_ask_value_fixtures(self)

  def tearDown(self):
    minimock.restore()

  def test_motes_open_non_exist(self):
    #self.cap_end()
    #print self.c.buffer

    # http://nullege.com/codes/show/src@burn-0.4.6@test@test_console.py

    expect_response = self.test_response

    m = Motes(motes_dir, 'open', 'something')

    assert_equal(expect_response, response)
"""

"""
Exec self
"""
if __name__ == '__main__':
  import nose

  nose.main()
