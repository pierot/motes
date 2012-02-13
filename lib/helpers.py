#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

"""
Helper functions
"""
def yes_no(msg):
  return True if raw_input('%s (y/n) ' % msg).lower() == 'y' else False

def yes_no_quit(msg):
  output = raw_input('%s (y/n/q) ' % msg).lower()
 
  if output == 'q':
    sys.exit()

  return True if output == 'y' else False
