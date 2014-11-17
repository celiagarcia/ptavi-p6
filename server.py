#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if line != "":
                print "El cliente nos manda " + line
                
                Metodo = line.split()[0]
                Sip = 'SIP/2.0 '
                # INVITE
                if Metodo == 'INVITE':
                    envio = Sip + '100 TRYING' + '\r\n'
                    envio += Sip + '180 RING' + '\r\n'
                    envio += Sip + '200 OK' + '\r\n'
                    self.wfile.write(envio)
                
                # BYE
                elif Metodo == 'BYE':
                    envio = Sip + '200 OK' + '\r\n'
                    self.wfile.write(envio)
                    
                # ACK
                elif Metodo == 'ACK':
                    print 'Comienza RTP'
                else:
                    envio = Sip + '405 Method Not Allowed'
                    self.wfile.write(envio)
                

            # Si no hay más líneas salimos del bucle infinito
            else:
                break

if __name__ == "__main__":

    try:
        # Puerto
        PORT = int(sys.argv[2])
        # IP
        IP = sys.argv[1]
        # Fichero
        Fich_audio = sys.argv[3]
    except ValueError:
        sys.exit('Usage: python server.py IP port audio_file')
    except IndexError:
        sys.exit('Usage: python server.py IP port audio_file')





    # Creamos servidor y escuchamos
    serv = SocketServer.UDPServer(("", PORT), EchoHandler)
    print "Listening..."
    serv.serve_forever()
