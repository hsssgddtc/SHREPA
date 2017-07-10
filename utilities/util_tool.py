# _*_ coding: utf-8 _*_

"""
util_parse.py by shai
"""

import logging

def SetupLogging(output_type):
  """S
  sets up logging for the spider.
  """
  if output_type == "console":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
  else:
    logging.basicConfig(filename = 'logs/SHREPA.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


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

