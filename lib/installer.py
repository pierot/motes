#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from os import environ, path

from helpers import *
from motes import CommandError, CommandLogger

"""
Install Motes and get installation directory
"""
class MotesInstaller:

  default_path = '.motes'
  config_file = '.motes'
  cmd_path = ''

  path = ''

  def __init__(self, cmd_path):
    self.cmd_path = cmd_path + '/'
    self.path = self.find_path()

  def installed(self):
    return self.path

  def install(self):
    CommandLogger('Motes wasn\'t installed yet.', True)
    
    do_install = yes_no_quit('Install Motes in your home directory (~/.motes)?')

    if do_install:
      self.set_path(environ['HOME'] + '/' + self.default_path)
    else:
      install_motes_path = raw_input('Where do you want Motes to be installed? Please give the full path, no ~. \'Motes\' directory will be created: ')

      if len(install_motes_path) > 0 and path.exists(install_motes_path):
        install_motes_path = path.normpath(install_motes_path + '/Motes')

        if pbs.mkdir(install_motes_path, '-p') == 0:
          self.set_path(install_motes_path)
        else:
          CommandError('Motes install directory could not be created. Permissions problem?', True).exe()
      else:
        CommandError('Given path did not exists.').exe()

  def config_path(self):
    return self.cmd_path + self.config_file

  def find_path(self):
    try:
      path_f = open(self.config_path(), 'r')
      target = path_f.read()

      path_f.close()

      if path.exists(target):
        return target + '/'
      else:
        return False
    except IOError:
      return False

  def set_path(self, target):
    try:
      path_f = open(self.config_path(), 'w')
      path_f.writelines(target)
      path_f.close()

      self.path = target
    except IOError:
      CommandError('Error installing Motes.').exe()

