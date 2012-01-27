#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import optparse
import datetime
import glob
import commands

from subprocess import call

from os.path import basename, isfile, exists, normpath
from os import environ

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
      CommandLogger("Invalid command given, use `" + ', '.join(Motes.commands().keys()) + "`")

      sys.exit()

    if isinstance(cmd, Command):
      try:
        cmd.exe()
      except Exception, e:
        print e.message

  def exec_command(self):
    return Motes.commands()[self.command](self, self.args)

  @staticmethod
  def commands():
    return {
      'create': CreateCommand, 
      'delete': DeleteCommand, 
      'find': FindCommand,
      'list': ListCommand, 
      'open': OpenCommand
    }


class CommandLogger:

  def __init__(self, message, sys=False):
    prefix = u'ە '.encode('utf-8') if sys else ''

    print '\033[94m' + prefix + message + '\033[0m'


class CommandError(Exception):
  
  def __init__(self, message):
    self.message = message

  def __str__(self):
    return repr('\033[91m' + self.message + '\033[0m')


class CommandExec:

  def __init__(self, cmd):
    [status, output] = commands.getstatusoutput(cmd)

    if status:
      CommandError(output)

      sys.exit()
    else:
      return output


class Command(object):
  
  def __init__(self, motes, args):
    self.args = args
    self.motes = motes

  def exe(self):
    raise NotImplementedError('Should have implemented this')


class OpenCommand(Command):

  def exe(self):
    if len(self.args) == 0:
      raise CommandError('No mote name given.')
    else:
      filename = self.args[0]
      filenr = int(filename) if filename.isdigit() else -1
     
      if filenr > -1:
        files = glob.glob(self.motes.home + '*')

        filepath = files[filenr] if len(files) > filenr else ""
        filename = basename(filepath)
      else:
        filepath = self.motes.home + filename

      if not isfile(filepath):
        make_msg = "Mote does not exist: do you want to create it?"
        make_file = yes_no(make_msg)
        
        if make_file:
          cmd = CreateCommand(self.motes, filename)
          cmd.exe()
      else:
        output = CommandExec('vim ' + filepath)

        if returncode == 0:
          CommandLogger('Mote closed.', True)


class CreateCommand(Command):

  def exe(self):
    filename = self.args[0] if type(self.args) == list else self.args
    filepath = self.motes.home + filename

    CommandLogger("Mote will create " + filename, True)

    output = CommandExec('touch ' + filepath)
    output = CommandExec('vim ' + filepath)


class DeleteCommand(Command):

  def exe(self):
    filename = self.args[0] if type(self.args) == list else self.args
    filenr = int(filename) if filename.isdigit() else -1
   
    if filenr > -1:
      files = glob.glob(self.motes.home + '*')

      filepath = files[filenr] if len(files) > filenr else ""
      filename = basename(filepath)
    else:
      filepath = self.motes.home + filename

    if isfile(filepath):
      delete_msg = 'Are you sure you want to delete ' + filename + '?'
      delete_file = yes_no(delete_msg)
    
      if delete_file:
        CommandExec('rm ' +  filepath)


class FindCommand(Command):

  def exe(self):
    search = self.args[0] if type(self.args) == list else self.args
    
    CommandLogger('Motes will search for ' + search, True)

    returncode = CommandExec('ack -a -i ' + search + ' ' + self.motes.home)


class ListCommand(Command):

  def exe(self):
    files = glob.glob(self.motes.home + '*')
   
    if len(files) > 0:
      CommandLogger("All motes\n", True)

    for idx, file in enumerate(files):
      CommandLogger("[" + str(idx) + "]\t" + basename(file))


class MotesInstaller:

  default_path = '.motes'
  config_path = '.motes'

  path = ''

  def __init__(self):
    self.path = self.find_path()

  def installed(self):
    return self.path

  def install(self):
    CommandLogger("Motes wasn't installed yet.", True)
    
    do_install = yes_no('Install Motes in your home directory (~/.motes)?')

    if do_install:
      self.set_path(environ['HOME'] + '/' + self.default_path)
    else:
      install_motes_path = raw_input("Where do you want Motes to be installed? Please give the full path, no ~. 'Motes' directory will be created: ")

      if len(install_motes_path) > 0 and exists(install_motes_path):
        install_motes_path = normpath(install_motes_path + '/Motes')

        if CommandExec('mkdir -p ' + install_motes_path) == 0:
          self.set_path(install_motes_path)
        else:
          CommandLogger('Motes install directory could not be created. Permissions problem?', True)

          sys.exit(0)
      else:
        CommandLogger('Given path did not exists.', True)

        sys.exit(0)

  def find_path(self):
    try:
      path_f = open('./' + self.config_path, 'r')
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
      path_f = open('./' + self.config_path, 'w')
      path_f.writelines(target)
      path_f.close()

      self.path = target
    except IOError:
      CommandLogger('Error installing Motes.', True)

##
# Helper functions
#
def yes_no(msg):
  return True if raw_input("%s (y/n) " % msg).lower() == 'y' else False

##
# Default init
#
if __name__ == '__main__':
  parser = optparse.OptionParser(usage='Usage: %prog [command] [options]', prog='Motes', version='%prog version 0.1')

  parser.add_option('-p', '--path', action="store_true", help='prints motes folder path')
  parser.add_option('-k', '--kitten', action="store_true", help='show me a kitten')

  (options, arguments) = parser.parse_args()

  mi = MotesInstaller()

  if not mi.installed():
    mi.install()

  if options.path:
    CommandLogger('Motes home directory: \n', True)
    CommandLogger(mi.path)
  elif options.kitten:
    CommandExec('open http://placekitten.com/800/600')
  else:
    if len(arguments) < 1:
      CommandLogger("Insufficient arguments given.", True)

      sys.exit()
    else: 
      m = Motes(mi.path, arguments[0], arguments[1::])
