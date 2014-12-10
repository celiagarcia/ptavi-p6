#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os
import os.path


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Server class
    """
    def handle(self):
        """
        Servidor de recepción que contesta a peticiones INVITE del cliente
        descargando un archivo mp3, y a peticiones BYE
        """
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if line != "":

                print "El cliente nos manda " + line

                linea = line.split()
                Metodo = line.split()[0]
                Sip = 'SIP/2.0 '
                # 400
                # otro or!!!!
                if len(linea) != 3 or linea[2] != 'SIP/2.0':
                    envio = Sip + '400 Bad Request' + '\r\n'
                    self.wfile.write(envio)

                # INVITE
                elif Metodo == 'INVITE':
                    envio = Sip + '100 TRYING' + '\r\n\r\n'
                    envio += Sip + '180 RINGING' + '\r\n\r\n'
                    envio += Sip + '200 OK' + '\r\n\r\n'
                    self.wfile.write(envio)

                # BYE
                elif Metodo == 'BYE':
                    envio = Sip + '200 OK' + '\r\n\r\n'
                    self.wfile.write(envio)

                # ACK
                elif Metodo == 'ACK':
                    aEjecutar = './mp32rtp -i 127.0.0.1 -p 23032 < '
                    aEjecutar += FICHERO
                    print 'Vamos a ejecutar ' + aEjecutar + '\r\n'
                    os.system(aEjecutar)
                    print 'Finaliza RTP' + '\r\n'
                # 405
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
        FICHERO = sys.argv[3]
        if os.path.exists(FICHERO) is False or len(sys.argv) != 4:
            print 'Usage: python server.py IP port audio_file'
            raise SystemExit
    except ValueError:
        sys.exit('Usage: python server.py IP port audio_file')
    except IndexError:
        sys.exit('Usage: python server.py IP port audio_file')

    # Creamos servidor y escuchamos
    serv = SocketServer.UDPServer(("", PORT), EchoHandler)
    print "Listening..."
    serv.serve_forever()
