"""
"""
import sys
import logging
import logging.config
from optparse import OptionParser
import socket


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('fileHandler')


def main(arguments):
    logging.info(f'Executing main: {arguments}')
    parser = OptionParser()
    parser.add_option('-r', '--remote', dest='remote',
                      default=False,
                      help='remote erver IP address')
    parser.add_option('-p', '--port', dest='port',
                      default=False,
                      help='remote server port')

    (options, args) = parser.parse_args(arguments)
    logging.info(f'Opt: {options} args: {args}')    



if __name__ == "__main__":
    main(sys.argv)
