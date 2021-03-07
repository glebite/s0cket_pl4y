# -*- coding: utf-8 -*-

"""
client.py
---------

This module implements code for learning about client connections,
threading, timers, connections, reconnections and state management.
"""

import sys
import logging
import logging.config
from optparse import OptionParser
import socket 

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('fileHandler')


class Client:
    """
    """
    def __init__(self, hostip, port):
        logging.info(f'Instantiation {self} hostip: {hostip} port: {port}')
        self.hostip = hostip
        self.port = port

    def run(self):
        """
        """
        logging.info('Running')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.hostip, self.port)
        pass


def usage():
    r"""Prints usage to stdout

    :param:  None
    :return: None
    """
    print('Usage: ')
    sys.exit(1)


def main(arguments):
    r"""Handles the processing of arguments and running the client.

    -s --server= ip address of the server to connect to
    -p --port=   port for the server

    :param:  arguments: command line arguments from sys.argv
    :return: None
    """
    logging.info(f'Executing main: {arguments}')
    parser = OptionParser()
    parser.add_option('-s', '--server', dest='server',
                      default=False,
                      help='server IP address')
    parser.add_option('-p', '--port', dest='port',
                      default=False,
                      help='server port')

    (options, args) = parser.parse_args(arguments)
    logging.info(f'Opt: {options} args: {args}')
    client = Client(options.server, int(options.port))
    client.run()
    logging.info('Completed execution')
    return None


if __name__ == "__main__":
    main(sys.argv)
