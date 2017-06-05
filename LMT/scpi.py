# coding: utf-8

# standard library
import sys
from socket import socket, AF_INET, SOCK_STREAM


# classes
class SCPI(object):
    """Create an interface to SCPI instruments.

    Args:
        host (str): An IP address of the instrument.
        port (int): A port number of the instrument.

    Example:
        >>> import scpi
        >>> FG = scpi.SCPI('192.168.1.2', port=8000)
        >>> FG.send('FREQ 10')
    """
    def __init__(self, host, port=8000):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((host, port))
        self.f = self.s.makefile('rb')

    def reset(self):
        self.s.send('*RST\n')
        self.s.send('*CLS\n')

    def send(self, command):
        print(command)
        self.s.send('{0}\n'.format(command))

    def get(self):
        c = self.s.recv(1024)
        print(c)
