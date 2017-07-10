# _*_ coding: utf-8 _*_

"""
util_parse.py by shai
"""

import logging

def SetupLogging():
  """S
  ets up logging for the spider.
  """

  logger = logging.getLogger('SHREPA')
  logger.setLevel(logging.DEBUG)

  console = logging.StreamHandler()
  level = logging.DEBUG
  console.setLevel(level)
  formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
  console.setFormatter(formatter)
  logger.addHandler(console)

