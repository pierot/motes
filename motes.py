#! /usr/bin/env python

import sys
import optparse
import datetime
import glob

from subprocess import call

from os.path import basename
from os.path import isfile

def main():
  usage = "Usage: %prog [command] [options]"
  p = optparse.OptionParser(usage, version='%prog version 0.1')

  (options, arguments) = p.parse_args()

  commands = ['create', 'delete', 'find', 'list', 'open']

  if len(arguments) < 1:
    print "Insufficient arguments given."

    sys.exit(0)
  
  if arguments[0] in commands:
    exec_command(arguments[0], arguments[1::])
  else:
    print "Invalid command given, use `" + ', '.join(commands) + "`"

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
  filepath = '/Users/pieterm/Dropbox/Private/notes/' + filename

  print "Mote will create " + filename

  call(['touch', filepath])

  call(['vim', filepath])

def exec_delete(args):
  filename = args[0] if type(args) == list else args
  filenr = int(filename) if filename.isdigit() else -1
 
  if filenr > -1:
    files = glob.glob('/Users/pieterm/Dropbox/Private/notes/*')

    filepath = files[filenr] if len(files) > filenr else ""
    filename = basename(filepath)
  else:
    filepath = '/Users/pieterm/Dropbox/Private/notes/' + filename

  if isfile(filepath):
    delete_msg = 'Are you sure you want to delete ' + filename + '?'
    delete_file = yes_no(delete_msg)
  
    if delete_file:
      call(['rm', filepath])

def exec_find(args):
  search = args[0] if type(args) == list else args
  
  print 'Motes will search for ' + search

  returncode = call(['ack', '-a', '-i', search, '/Users/pieterm/Dropbox/Private/notes'])

def exec_list(args):
  files = glob.glob('/Users/pieterm/Dropbox/Private/notes/*')
 
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
    filepath = '/Users/pieterm/Dropbox/Private/notes/' + filename

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
