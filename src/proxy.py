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
    pass


if __name__ == "__main__":
    main(sys.argv)
