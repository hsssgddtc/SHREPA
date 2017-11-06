# _*_ coding: utf-8 _*_

"""
util_parse.py by shai
"""

import logging
import os
import sys
import time


ISOTIMEFORMAT='%Y%m%d'

def SetupLogging(output_type):
  """
  Sets up logging for the spider.
  """
  log_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/logs/SHREPA_"+str(time.strftime(ISOTIMEFORMAT))+".log"
  if output_type == "console":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
  else:
    logging.basicConfig(filename = log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def HandleDaemon(handle_type):
  """
    Create daemon file for process.
  """
  pidfile = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/mydaemon.pid"

  if handle_type == "create":
    pid = str(os.getpid())
    if os.path.isfile(pidfile):
      print "%s already exists, exiting" % pidfile
      sys.exit()
    file(pidfile, 'w').write(pid)

  if handle_type == "delete":
    os.unlink(pidfile)
  #logger = logging.getLogger('SHREPA')
  ##logger.setLevel(logging.DEBUG)
  #
  #console = logging.StreamHandler()
  #level = logging.DEBUG
  #console.setLevel(level)
  #formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
  #console.setFormatter(formatter)
  #logger.addHandler(console)
  #
  #logger.debug("test")
  #
  #return logger

