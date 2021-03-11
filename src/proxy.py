"""
"""
import sys
import logging
import logging.config
from optparse import OptionParser
import socket


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('fileHandler')


class Proxy(object):
    def __init__(self, arguments):
        """__init__

        :param:  arguments - argument dictionary for configuration
        :return: None
        """
        pass

    def loop(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server.socket.bind((self.localhost, self.localport))
        except:
            sys.exit(0)

        while True:
            try:
                self.client_socket, self.addr = self.server_socket.accept()
            except:
                pass
            self.proxy_thread = threading.Thread(target=self.proxy_handler)
            self.proxy_thread.start()

    def proxy_handler(self):
        pass
    

def main(arguments):
    logging.info(f'Executing main: {arguments}')
    parser = OptionParser()
    parser.add_option('-r', '--remote', dest='remote',
                      default=False,
                      help='remote server IP address')
    parser.add_option('-p', '--port', dest='port',
                      default=False,
                      help='remote server port')
    parser.add_option('-c', '--client', dest='client',
                      default=False,
                      help='client server IP address')
    parser.add_option('-P', '--Port', dest='client_port',
                      default=False,
                      help='client server port')
    
    (options, args) = parser.parse_args(arguments)
    logging.info(f'Opt: {options} args: {args}')    



if __name__ == "__main__":
    main(sys.argv)
