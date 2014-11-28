#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
import os

# Cliente UDP simple.

Metodos = ['INVITE', 'BYE']

try:
    # Metodo
    METODO = sys.argv[1].upper()
    # Información del receptor
    INFOR = sys.argv[2]
    PORT = int(sys.argv[2].split('@')[1].split(':')[1])
    SERVER_IP = sys.argv[2].split('@')[1].split(':')[0]
    if len(sys.argv) != 3:
        print 'Usage: python client.py method receiver@IP:SIPport'
        raise SystemExit
except ValueError:
    sys.exit('Usage: python client.py method receiver@IP:SIPport')
except IndexError:
    sys.exit('Usage: python client.py method receiver@IP:SIPport')

# Contenido que vamos a enviar
DIRECCION = INFOR.split(':')[0]
LINE = METODO + ' sip:' + DIRECCION + ' SIP/2.0'

try:
    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER_IP, PORT))

    print "Enviando: " + LINE + '\r\n'
    my_socket.send(LINE + '\r\n')
    data = my_socket.recv(1024)

    print 'Recibido -- ' + '\r\n', data

    datos = data.split()

    # Procesando las respuestas
    Sip = 'SIP/2.0 '
    if datos[1] == '100' and datos[4] == '180' and datos[7] == '200':
        LINE = 'ACK SIP:' + DIRECCION + ' SIP/2.0'
        print "Enviando: " + LINE + '\r\n'
        my_socket.send(LINE + '\r\n')

    # Cerramos todo
    my_socket.close()
    print "Fin."
except socket.gaierror:
    com = 'Error: No server listening at '
    sys.exit(com + SERVER_IP + ' port ' + str(PORT))
except socket.error:
    com = 'Error: No server listening at '
    sys.exit(com + SERVER_IP + ' port ' + str(PORT))
