# coding: utf-8

# standard library
import sys
import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM


# classes
class SCPI(socket.socket):
    """Create an interface to SCPI instruments.

    Args:
        host (str): An IP address of the instrument.
        port (int): A port number of the instrument.

    Example:
        >>> import scpi
        >>> FG = scpi.SCPI('192.168.1.2', port=8000)
        >>> FG.send('FREQ 10')
    """
    def __init__(self, host, port=8000, protocol='TCP'):
        if protocol == 'TCP':
            super(SCPI, self).__init__(AF_INET, SOCK_STREAM)
            self.connect((host, port))
        elif protocol == 'UDP':
            super(SCPI, self).__init__(AF_INET, SOCK_DGRAM)
        else:
            raise ValueError(protocol)

        self.info = {
            'host': host,
            'port': port,
            'protocol': protocol,
            'pythonver': sys.version_info.major
        }

    def send(self, command):
        # make a sending data as bytes
        if self.info['pythonver'] == 2:
            senddata = '{0}\n'.format(command)
        elif self.info['pythonver'] == 3:
            senddata = '{0}\n'.format(command).encode('utf-8')

        # send data
        if self.info['protocol'] == 'TCP':
            super(SCPI, self).send(senddata)
        elif self.info['protocol'] == 'UDP':
            address = (self.info['host'], self.info['port'])
            super(SCPI, self).sendto(senddata, address)

        # print status
        print('SEND> {0}'.format(command))
        if command.endswith('?') or (self.info['protocol'] == 'UDP'):
            recvdata = self.get()
            print('RECV> {0}'.format(recvdata))

    def get(self):
        if self.info['pythonver'] == 2:
            return self.recv(1024)
        elif self.info['pythonver'] == 3:
            return self.recv(1024).decode('utf-8')

    def reset(self):
        if self.info['protocol'] == 'UDP':
            raise UserWarning('this method is for TCP only!')

        self.send('*RST\n')
        self.send('*CLS\n')
