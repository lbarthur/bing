#python3
#openssl req -x509 -days 3650 -nodes -sha256 -newkey rsa:2048 -keyout key.pem -out cert.pem
import http.server, ssl

server_address = ('0.0.0.0', 20443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket,
                               server_side=True,
                               certfile='/reboot/logs/cert.pem',
                               keyfile='/reboot/logs/key.pem',
                               ssl_version=ssl.PROTOCOL_TLSv1_2)
httpd.serve_forever()


'''
#python2
import BaseHTTPServer, SimpleHTTPServer
import ssl

httpd = BaseHTTPServer.HTTPServer(('localhost', 20443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, server_side=True,
                                certfile='/reboot/logs/cert.pem')
httpd.serve_forever()
'''