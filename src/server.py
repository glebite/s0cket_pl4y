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
from os import path

log_file_path = path.join(path.dirname(path.abspath("__file__")),
                          'logging.conf')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger('fileHandler')


class Error(Exception):
    """ """
    pass


class ThreadedServer(object):
    def __init__(self, host, port):
        """__init__ - initialization method for ThreadedServer

        :param:  host - host location of this server
        :param:  port - port of the server
        :return: None
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.counter = 0
        self.clients = []

    def listen(self):
        """listen - listening to incoming connection
        """
        self.sock.listen(5)
        while True:
            logging.debug(f'Incoming connect counter: {self.counter}')
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listenToClient,
                             args=(client, address)).start()
            self.counter += 1

    def listen_to_client(self, client, address):
        """listen_to_client - data retrieval magic

        :param:  client - 
        :param:  address -
        :return: False in an error
        """
        logging.info(f'Thread counter: {self.counter}')
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    response = data
                    client.send(response)
                else:
                    logging.error('In the else case - nothing received?')
                    raise Exception
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


if (__name__ == "__main__"):
    main(sys.argv)
