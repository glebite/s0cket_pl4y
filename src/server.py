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
import socket

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

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), 5150))
    server_socket.listen(5)
    return None


if __name__ == "__main__":
    main(sys.argv)
