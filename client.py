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
    METODO = sys.argv[1]
    """
    if not METODO in Metodos:
        print 'Usage: python client.py method receiver@IP:SIPport'
        raise SystemExit 
    """
    # Información del receptor
    INFOR = sys.argv[2]
    PORT = int(sys.argv[2].split('@')[1].split(':')[1])
    SERVER_IP = sys.argv[2].split('@')[1].split(':')[0]
except ValueError:
    sys.exit('Usage: python client.py method receiver@IP:SIPport')
except IndexError:
    sys.exit('Usage: python client.py method receiver@IP:SIPport')



# Contenido que vamos a enviar
DIRECCION = INFOR.split(':')[0]
LINE = METODO + ' sip:' + DIRECCION + ' SIP/2.0\r\n'


try:
    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER_IP, PORT))


    print "Enviando: " + LINE
    my_socket.send(LINE + '\r\n')
    data = my_socket.recv(1024)

    print 'Recibido -- ' + '\r\n', data
    
    datos =  data.split()
    
    # Procesando las respuestas
    Sip = 'SIP/2.0 '
    if datos[1] == '100' and datos[4] == '180' and datos[7] == '200':
        LINE = 'ACK SIP:' + DIRECCION + ' SIP/2.0'
        print "Enviando: " + LINE
        my_socket.send(LINE + '\r\n')
        data = my_socket.recv(1024)
        
        print 'Comienza RTP'
        
    """    
    elif datos[1] = '200':
        
    elif datos[1] == '400':
    
    elif datos[1] == '405':
        
    print "Terminando socket..."
    """
    
    # Cerramos todo
    my_socket.close()
    print "Fin."
    
except socket.gaierror:
    sys.exit('Error: No server listening at ' + SERVER_IP +' port ' + str(PORT))
except socket.error:
    sys.exit('Error: No server listening at ' + SERVER_IP +' port ' + str(PORT))

