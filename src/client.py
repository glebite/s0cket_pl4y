# -*- coding: utf-8 -*-

"""
client.py
---------

This module implements code for learning about client connections,
threading, timers, connections, reconnections and state management.
"""

import sys
import getopt


class Client:
    """
    """
    def __init__(self, hostip, port):
        self.hostip = hostip
        self.port = port

    def run(self):
        """
        """
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
    options, _ = getopt.getopt(arguments,
                               'hs:p:', ['server=', 'port='])
    for opt, arg in options:
        if opt in ('-s', '--server'):
            server = arg
        elif opt in ('-p', '--port'):
            port = int(arg)
        elif opt in ('-h'):
            usage()
        else:
            usage()
    client = Client(server, port)
    client.run()
    return None


if __name__ == "__main__":
    main(sys.argv)
