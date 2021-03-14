"""
"""
import sys
import logging
import logging.config
from optparse import OptionParser
import socket
import threading


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('fileHandler')


class Proxy(object):
    def __init__(self, arguments):
        """__init__

        :param:  arguments - argument dictionary for configuration
        :return: None
        """
        self.timeout = 2
        self.buffer_size = 1024

        # tease data members from arguments
        logging.debug(f'Arguments: {arguments}')
        self.localhost = arguments.local
        self.localport = int(arguments.local_port)
        self.remote_ip = arguments.remote_ip
        self.remote_port = int(arguments.remote_port)

    def loop(self):
        """loop

        :param:  None
        :return: None
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server_socket.bind((self.localhost, self.localport))
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
        try:
            socket.settimeout(self.timeout)
            data_buffer = b""
            while True:
                data = socket.recv(self.buffer_size)
                if not data:
                    break
                data_buffer += data
        except Exception as e:
            print(f"[!] Socket Error {e}")
            pass
        return data_buffer

    def proxy_handler(self):
        """proxy_handler
        :param:  None
        :return: None
        """
        self.remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_socket.connect((self.remote_ip, self.remote_port))

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
    parser.add_option('-r', '--remote', dest='remote_ip',
                      default=False,
                      help='remote server IP address')
    parser.add_option('-p', '--port', dest='remote_port',
                      default=False,
                      help='local server port')
    parser.add_option('-c', '--local', dest='local',
                      default=False,
                      help='local server IP address')
    parser.add_option('-P', '--Port', dest='local_port',
                      default=False,
                      help='local server port')
    (options, args) = parser.parse_args(arguments)
    logging.info(f'Opt: {options} args: {args}')
    proxy = Proxy(options)
    proxy.run()


if __name__ == "__main__":
    main(sys.argv)
