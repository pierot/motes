#! /usr/bin/env python

import sys
import optparse
import datetime
import glob

from os.path import basename

def main():
  usage = "Usage: %prog [command] [options]"
  p = optparse.OptionParser(usage, version='%prog version 0.1')

  (options, arguments) = p.parse_args()

  commands = ['create', 'find', 'list', 'open']

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
    'find': exec_find,
    'list': exec_list, 
    'open': exec_open
  }[command](args)

def exec_create(args):
  print args

def exec_find(args):
  print args

def exec_list(args):
  files = glob.glob('/Users/pieterm/Dropbox/Private/notes/*')
 
  if len(files) > 0:
    print "All motes\n"

  for idx, file in enumerate(files):
    print "[" + str(idx) + "]\t" + basename(file)

def exec_open(args):
  print args

# Default init
if __name__ == '__main__':
  main()
