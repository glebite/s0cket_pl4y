#!/usr/bin/env python
"""
proxy.py
"""
import sys
import logging
import logging.config
import socket
import threading
from optparse import OptionParser


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('fileHandler')


class Proxy(object):
    def __init__(self, arguments):
        """__init__

        :param:  arguments - argument object for configuration
                             .local_host = the host of the proxy 
                             .local_port = the port to access the proxy 
                              (needs to be converted to an int)
                             .remote_host = the destination host to use 
                             .remote_port = the destination port to use
                              (needs to be converted to an int)
        :return: None
        """
        # tease data members from arguments
        logging.debug(f'Arguments: {arguments}')
        self.local_host = arguments.local_host
        self.local_port = int(arguments.local_port)
        self.remote_host = arguments.remote_host
        self.remote_port = int(arguments.remote_port)
        
        self.socket_timeout = 0.01
        self.buffer_size = 1024
        self.pending_connections = 1



    def loop(self):
        """loop

        :param:  None
        :return: None
        """
        logging.info(f'Socket instantiation loop: '
                     f'local_host: {self.local_host}'
                     f'local_port: {self.local_port}'
                     f'pending_connections: {self.pending_connections}'
                     f'proxy_handler = {self.proxy_handler}')
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug(f'Socket creation: {self.server_socket}')

        # This allows for reuse of the port connection
        self.server_socket.setsockopt(socket.SOL_SOCKET,
                                      socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.local_host, self.local_port))
            self.server_socket.listen(self.pending_connections)
        except Exception as e:
            logging.error(f'Loop socket bind: {e}')
            sys.exit(0)

        while True:
            try:
                self.client_socket, self.addr = self.server_socket.accept()
            except Exception as e:
                logging.error(f'Socket accept: {e}.')
            self.proxy_thread = threading.Thread(target=self.proxy_handler)
            self.proxy_thread.start()

    def receive_from(self, socket):
        """receive_from

        :param:   socket - socket used for receiving data
        :return:  data_buffer - binary string containing
                                data read from the socket.
        """
        socket.settimeout(self.socket_timeout)
        try:
            data_buffer = b""
            while True:
                received_data = socket.recv(self.buffer_size)
                if not received_data:
                    break
                logging.debug(f'Received data: {received_data}')
                data_buffer += received_data
        except Exception:
            # logging.error(f"[!] Socket Error {e}")
            pass
        return data_buffer

    def proxy_handler(self):
        """proxy_handler
        :param:  None
        :return: None
        """
        logging.info('Coming into proxy_handler.')
        self.remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_socket.connect((self.remote_host, self.remote_port))

        while True:
            local_buffer = self.receive_from(self.client_socket)
            if len(local_buffer) > 0:
                self.remote_socket.send(local_buffer)
            remote_buffer = self.receive_from(self.remote_socket)
            if len(remote_buffer) > 0:
                self.client_socket.send(remote_buffer)

    def run(self):
        """run
        """
        self.loop()


def main(arguments):
    """main

    :param:  arguments
    :return: None
    """
    logging.info(f'Executing main: {arguments}')
    parser = OptionParser()
    parser.add_option('-r', '--remote', dest='remote_host',
                      default=False,
                      help='remote server IP address')
    parser.add_option('-p', '--port', dest='remote_port',
                      default=False,
                      help='local server port')
    parser.add_option('-c', '--local', dest='local_host',
                      default=False,
                      help='local server IP address')
    parser.add_option('-P', '--Port', dest='local_port',
                      default=False,
                      help='local server port')
    (options, args) = parser.parse_args(arguments)
    logging.debug(f'Opt: {options} args: {args}')
    proxy = Proxy(options)
    proxy.run()


if __name__ == "__main__":
    main(sys.argv)
