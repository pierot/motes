# -*- coding: utf-8 -*-

import sys
import glob
import pbs
import re
import urllib
import base64

from os import environ, path

from helpers import *

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
      'reveal': RevealCommand,
      'share': ShareCommand
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

  @property
  def filename(self):
    filename = self.args[0] if type(self.args) == list else self.args
    filenr = int(filename) if filename.isdigit() else -1
   
    if filenr > -1:
      files = glob.glob(self.motes_path + '*')

      filepath = files[filenr] if len(files) > filenr else ''
      filename = path.basename(filepath)
    else:
      filename = PathCleaner(filename).long()

    return filename

  def exe(self):
    raise NotImplementedError('Should have implemented this')


"""
Opens Motes site
"""
class SiteCommand(Command):
  
  def exe(self):
    CommandLogger('Motes site is opening ..', True)

    pbs.open('http://0.0.0.0:3000', _fg=True)

    from web.motes import motes_web_start
    
    motes_web_start(self.motes_path)

"""
Open a Mote
"""
class OpenCommand(Command):

  def exe(self):
    if len(self.args) == 0:
      SiteCommand(self.motes_path, None).exe()
    else:
      filepath = self.motes_path + self.filename

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
class ShareCommand(Command):

  def exe(self):
    CommandLogger('Sharing `' + self.filename + '`.\n', True)    
   
    c = ContentCommand(self.motes_path, self.filename)
     
    file_content = c.contents if len(c.contents) > 0 else ' '

    #file_unescaped_encoded = urllib.quote(self.encodeURIComponent(file_content))
    file_unescaped_encoded = file_content
    file_base64_encoded = base64.b64encode(file_unescaped_encoded)
    
    share_url = 'http://hashify.me/' + file_base64_encoded

    CommandLogger(share_url)

    pbs.open(share_url)

  def encodeURIComponent(self, str):
    def replace(match):
      return "%" + hex( ord( match.group() ) )[2:].upper()

    return re.sub(r"([^0-9A-Za-z!'()*\-._~])", replace, str.encode('utf-8') ) 


"""
Fetch motes content
"""
class ContentCommand(Command):

  def exe(self):
    CommandLogger('Contents of `' + self.filename + '`.\n', True)    
    
    file_content = self.contents

    if not file_content:
      print '# File not found'
    else:
      print file_content

  @property
  def contents(self):
    filepath = self.motes_path + self.filename
    
    if not path.isfile(filepath):
      output = False
    else:
      output = open(filepath, 'r').read()

    return output


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
    filepath = self.motes_path + self.filename

    if path.isfile(filepath):
      delete_msg = 'Are you sure you want to delete the mote named `' + PathCleaner(self.filename).short() + '`?'
      delete_file = yes_no(delete_msg)
    
      if delete_file:
        pbs.rm(filepath)


"""
Finds (a) Mote(s) based on a string. Can be a regular expression as well
"""
class FindCommand(Command):

  def exe(self):
    search = self.args[0] if type(self.args) == list else self.args
    search_string = search + ' ' + self.motes_path 

    CommandLogger('Motes will search for `' + search + '` in your motes', True)
    
    result = pbs.ack(search_string, '-a', '-i', '-u', '--flush', '--nopager', _fg=True)

    print result


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
