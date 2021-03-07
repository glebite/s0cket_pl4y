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
import threading

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('fileHandler')


class Error(Exception):
    pass


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listenToClient,
                             args=(client, address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    response = data
                    client.send(response)
                else:
                    raise Error
            except Exception as e:
                logging.error(f'Problem while listening to the client: {e}')
                client.close()
                return False


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
    t = ThreadedServer('0.0.0.0', int(options.port))
    t.listen()
    return None


if __name__ == "__main__":
    main(sys.argv)
