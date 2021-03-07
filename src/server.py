# -*- coding: utf-8 -*-

"""
server.py
---------

This module implements code for learning about server connections,
threading, timers, connections, reconnections and state management.


"""

import sys
import logging
import logging.config
from optparse import OptionParser

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('fileHandler')


def main(arguments):
    r"""Handles the processing of arguments and running the server.

    :param arguments: command line arguments from sys.argv
    :return: None
    """
    parser = OptionParser()
    parser.add_option('-p', '--port', dest='port',
                      default=False,
                      help='server port')
    (options, args) = parser.parse_args(arguments)
    logging.info(f'Port: {int(options.port)}')
    return None


if __name__ == "__main__":
    main(sys.argv)
