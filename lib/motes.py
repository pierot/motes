# -*- coding: utf-8 -*-

import sys
import glob
import pbs

from os import environ, path

"""
Motes class. Needs to know:
  * where the Motes are located
  * a command 
  * and maybe some arguments
"""
class Motes:

  home = ''
  command = ''

  ext = '.md'

  def __init__(self, home_path, command, args):
    self.command = command
    self.args = args
    self.home = home_path
  
    try:
      cmd = self.fetch_command()
    except KeyError, e:
      CommandLogger('Invalid command given')
      CommandLogger(', use `' + ', '.join(Motes.commands().keys()) + '`')

      sys.exit()

    if isinstance(cmd, Command):
      try:
        cmd.exe()
      except Exception, e:
        CommandError(e.message).exe()

  def fetch_command(self):
    return Motes.commands()[self.command](self.home, self.args)

  @staticmethod
  def commands():
    return {
      'create': CreateCommand, 
      'delete': DeleteCommand, 
      'find': FindCommand,
      'list': ListCommand, 
      'open': OpenCommand,
      'print': ContentCommand,
      'reveal': RevealCommand
    }


"""
Path filename cleaning class
"""
class PathCleaner:

  def __init__(self, filename):
    self.file_name, self.file_ext = path.splitext(filename)
    self.file_ext = self.file_ext if len(self.file_ext) > 0 else Motes.ext

  def short(self):
    return self.file_name

  def long(self):
    return self.file_name + self.file_ext

  def ext(self):
    return self.file_ext


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

  def exe(self, error_code=1):
    print self

    sys.exit(error_code)

  def __str__(self):
    prefix = u'ە '.encode('utf-8')

    return '\033[91m' + prefix + self.message + '\033[0m'


"""
Parent class of all Motes commands
"""
class Command(object):
  
  def __init__(self, motes_path, args):
    self.args = args
    self.motes_path = motes_path

  def exe(self):
    raise NotImplementedError('Should have implemented this')


"""
Opens Motes site
"""
class SiteCommand(Command):
  
  def exe(self):
    CommandLogger('Motes site is opening ..', True)

    from web.motes import motesite
    
    motesite.run(host='0.0.0.0', port=3000)
 
    pbs.open('http://0.0.0.0:3000', _fg=True)


"""
Open a Mote
"""
class OpenCommand(Command):

  def exe(self):
    if len(self.args) == 0:
      SiteCommand(self.motes_path, None).exe()
    else:
      filename = self.args[0]
      filenr = int(filename) if filename.isdigit() else -1
     
      if filenr > -1:
        files = glob.glob(self.motes_path + '*')

        filepath = files[filenr] if len(files) > filenr else ''
        filename = path.basename(filepath)
      else:
        filename = PathCleaner(filename).long()
        filepath = self.motes_path + filename

      if not path.isfile(filepath):
        make_msg = 'Mote does not exist: do you want to create it?'
        make_file = yes_no(make_msg)
        
        if make_file:
          cmd = CreateCommand(self.motes_path, filename)
          cmd.exe()
      else:
        output = pbs.vim(filepath, _fg=True)

        if output == 0:
          CommandLogger('Mote closed.', True)


"""
Fetch motes content
"""
class ContentCommand(Command):

  def exe(self):
    CommandLogger('Contents of `' + self.file_name() + '`.\n', True)    
    
    contents = self.get_content()

    if not contents:
      print '# File not found'
    else:
      print contents

  def get_content(self):
    filepath = self.motes_path + self.file_name()
    
    if not path.isfile(filepath):
      output = False
    else:
      output = open(filepath, 'r').read()

    return output

  def file_name(self):
    filename = self.args[0] if type(self.args) == list else self.args

    return PathCleaner(filename).long()
    

"""
Creates a Mote
"""
class CreateCommand(Command):

  def exe(self):
    filename = self.args[0] if type(self.args) == list else self.args
    filename = PathCleaner(filename).long()
    filepath = self.motes_path + filename

    CommandLogger('Motes will create a new mote name `' + PathCleaner(filename).short() + '`', True)

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
      files = glob.glob(self.motes_path + '*')

      filepath = files[filenr] if len(files) > filenr else ''
      filename = path.basename(filepath)
    else:
      filename = PathCleaner(filename).long()
      filepath = self.motes_path + filename

    if path.isfile(filepath):
      delete_msg = 'Are you sure you want to delete the mote named `' + PathCleaner(filename).short() + '`?'
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

    pbs.ack(search + ' ' + self.motes_path, '-a', '-i')


"""
List all Motes
"""
class ListCommand(Command):

  def exe(self):
    files = self.files()
   
    if len(files) > 0:
      CommandLogger('All motes\n', True)

    for idx, file in enumerate(files):
      CommandLogger('[' + str(idx) + ']\t' + PathCleaner(path.basename(file)).short())

  def files(self):
    raw_files = glob.glob(self.motes_path + '*')
    files = []

    for idx, file in enumerate(raw_files):
      files.append(path.basename(file))

    return files


"""
Reveal the motes folder in Finder
"""
class RevealCommand(Command):

  def exe(self):
    pbs.open(self.motes.home)

    CommandLogger('All your motes are belong to Finder.', True)


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
