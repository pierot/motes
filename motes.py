#! /usr/bin/env python

import sys
import optparse
import datetime
import glob

from subprocess import call

from os.path import basename
from os.path import isfile
from os.path import exists
from os import environ

def main():
  usage = "Usage: %prog [command] [options]"
  p = optparse.OptionParser(usage, version='%prog version 0.1')

  (options, arguments) = p.parse_args()

  commands = ['create', 'delete', 'find', 'list', 'open']

  if not motes_home():
    install_motes()

  if len(arguments) < 1:
    print "Insufficient arguments given."

    sys.exit(0)
  
  if arguments[0] in commands:
    exec_command(arguments[0], arguments[1::])
  else:
    print "Invalid command given, use `" + ', '.join(commands) + "`"

def install_motes():
  print "Motes wan't installed yet."
  
  install_motes_home = yes_no('Install Motes in your home directory (~/.motes)?')

  if install_motes_home:
    set_motes_home(environ['HOME'] + '/.motes')
  else:
    install_motes_path = raw_input("Where do you want Motes to be installed? Please give the full path, no ~. 'Motes' directory will be created: ")

    if len(install_motes_path) > 0 and exists(install_motes_path):
      install_motes_path = install_motes_path + '/Motes'

      if call(['mkdir', '-p', install_motes_path]) == 0:
        set_motes_home(install_motes_path)
      else:
        print 'Motes install directory could not be created. Permissions problem?'

        sys.exit(0)
    else:
      print 'Given path did not exists.'

      sys.exit(0)

def motes_home():
  try:
    path_f = open('./.motes', 'r')
    target = path_f.read()
    path_f.close()

    return target + '/'
  except IOError:
    return False

def set_motes_home(target):
  try:
    path_f = open('./.motes', 'w')
    path_f.writelines(target)
    path_f.close()
  except IOError:
    print 'Error installing motes.'

def exec_command(command, args):
  return {
    'create': exec_create, 
    'delete': exec_delete, 
    'find': exec_find,
    'list': exec_list, 
    'open': exec_open
  }[command](args)

def exec_create(args):
  filename = args[0] if type(args) == list else args
  filepath = motes_home() + filename

  print "Mote will create " + filename

  call(['touch', filepath])

  call(['vim', filepath])

def exec_delete(args):
  filename = args[0] if type(args) == list else args
  filenr = int(filename) if filename.isdigit() else -1
 
  if filenr > -1:
    files = glob.glob(motes_home() + '*')

    filepath = files[filenr] if len(files) > filenr else ""
    filename = basename(filepath)
  else:
    filepath = motes_home() + filename

  if isfile(filepath):
    delete_msg = 'Are you sure you want to delete ' + filename + '?'
    delete_file = yes_no(delete_msg)
  
    if delete_file:
      call(['rm', filepath])

def exec_find(args):
  search = args[0] if type(args) == list else args
  
  print 'Motes will search for ' + search

  returncode = call(['ack', '-a', '-i', search, motes_home()])

def exec_list(args):
  files = glob.glob(motes_home() + '*')
 
  if len(files) > 0:
    print "All motes\n"

  for idx, file in enumerate(files):
    print "[" + str(idx) + "]\t" + basename(file)

def exec_open(args):
  if len(args) == 0:
    print "No note name given."

    sys.exit(0)
  else:
    filename = args[0]
    filepath = motes_home() + filename

    if not isfile(filepath):
      make_msg = "Note does not exist: do you want to create it?"
      make_file = yes_no(make_msg)
      
      if make_file:
        exec_create(filename)
    else:
      returncode = call(['vim', filepath])

      if returncode == 0:
        print 'Mote note closed.'

def yes_no(msg):
  return True if raw_input("%s (y/n) " % msg).lower() == 'y' else False

# Default init
if __name__ == '__main__':
  main()
