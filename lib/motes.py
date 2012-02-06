# -*- coding: utf-8 -*-

import sys
import glob
import pbs
import subprocess

from os.path import basename, isfile, exists, normpath
from os import environ

"""
Motes class. Needs to know where the Motes are located,
a command and maybe some arguments
"""
class Motes:

  home = ''
  command = ''

  def __init__(self, home_path, command, args):
    self.command = command
    self.args = args
    self.home = home_path
  
    try:
      cmd = self.exec_command()
    except KeyError, e:
      CommandLogger('Invalid command given')
      CommandLogger(', use `' + ', '.join(Motes.commands().keys()) + '`')

      sys.exit()

    if isinstance(cmd, Command):
      try:
        cmd.exe()
      except Exception, e:
        raise CommandError(e.message)

  def exec_command(self):
    return Motes.commands()[self.command](self, self.args)

  @staticmethod
  def commands():
    return {
      'create': CreateCommand, 
      'delete': DeleteCommand, 
      'find': FindCommand,
      'list': ListCommand, 
      'open': OpenCommand,
      'reveal': RevealCommand
    }


"""
Central logger class
"""
class CommandLogger:

  def __init__(self, message, sys=False):
    prefix = u'ە '.encode('utf-8') if sys else ''

    print '\033[94m' + prefix + message + '\033[0m'


"""
Error class for all Motes errors
"""
class CommandError(Exception):
  
  def __init__(self, message):
    self.message = message

  def __str__(self):
    prefix = u'ە '.encode('utf-8')

    return '\033[91m' + prefix + self.message + '\033[0m'


"""
Parent class of all Motes commands
"""
class Command(object):
  
  def __init__(self, motes, args):
    self.args = args
    self.motes = motes

  def exe(self):
    raise NotImplementedError('Should have implemented this')


"""
Open a Mote
"""
class OpenCommand(Command):

  def exe(self):
    if len(self.args) == 0:
      raise CommandError('No mote name given.')
    else:
      filename = self.args[0]
      filenr = int(filename) if filename.isdigit() else -1
     
      if filenr > -1:
        files = glob.glob(self.motes.home + '*')

        filepath = files[filenr] if len(files) > filenr else ''
        filename = basename(filepath)
      else:
        filepath = self.motes.home + filename

      if not isfile(filepath):
        make_msg = 'Mote does not exist: do you want to create it?'
        make_file = yes_no(make_msg)
        
        if make_file:
          cmd = CreateCommand(self.motes, filename)
          cmd.exe()
      else:
        output = pbs.vim(filepath, _fg=True)

        if output == 0:
          CommandLogger('Mote closed.', True)


"""
Creates a Mote
"""
class CreateCommand(Command):

  def exe(self):
    filename = self.args[0] if type(self.args) == list else self.args
    filepath = self.motes.home + filename

    CommandLogger('Motes will create a new mote name `' + filename + '`', True)

    pbs.touch(filepath) # create it anyway
    pbs.vim(filepath, _fg=True)


"""
Deletes a Mote
"""
class DeleteCommand(Command):

  def exe(self):
    filename = self.args[0] if type(self.args) == list else self.args
    filenr = int(filename) if filename.isdigit() else -1
   
    if filenr > -1:
      files = glob.glob(self.motes.home + '*')

      filepath = files[filenr] if len(files) > filenr else ''
      filename = basename(filepath)
    else:
      filepath = self.motes.home + filename

    if isfile(filepath):
      delete_msg = 'Are you sure you want to delete the mote named `' + filename + '`?'
      delete_file = yes_no(delete_msg)
    
      if delete_file:
        pbs.rm(filepath)


"""
Finds (a) Mote(s) based on a string. Can be a regular expression as well
"""
class FindCommand(Command):

  def exe(self):
    search = self.args[0] if type(self.args) == list else self.args
    
    CommandLogger('Motes will search for `' + search + '` in your motes', True)

    pbs.ack(search + ' ' + self.motes.home, '-a', '-i')


"""
List all Motes
"""
class ListCommand(Command):

  def exe(self):
    files = glob.glob(self.motes.home + '*')
   
    if len(files) > 0:
      CommandLogger('All motes\n', True)

    for idx, file in enumerate(files):
      CommandLogger('[' + str(idx) + ']\t' + basename(file))

"""
Reveal the motes folder in Finder
"""
class RevealCommand(Command):

  def exe(self):
    self.motes.home

    pbs.open(self.motes.home)

    CommandLogger('All your motes are belong to Finder\n', True)

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

      if len(install_motes_path) > 0 and exists(install_motes_path):
        install_motes_path = normpath(install_motes_path + '/Motes')

        if pbs.mkdir(install_motes_path, '-p') == 0:
          self.set_path(install_motes_path)
        else:
          print CommandError('Motes install directory could not be created. Permissions problem?', True)

          sys.exit(0)
      else:
        print CommandError('Given path did not exists.')

        sys.exit(0)

  def config_path(self):
    return self.cmd_path + self.config_file

  def find_path(self):
    try:
      path_f = open(self.config_path(), 'r')
      target = path_f.read()

      path_f.close()

      if exists(target):
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
      print CommandError('Error installing Motes.')

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
