# coding: utf-8
#--------------
import socket
import parserRequest
import httpStatus

HOST = ''
PORT = 8888
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

print 'Serving HTTPServer at http://127.0.0.1:%s ...' % PORT

def openFile(filePath):
    f = open(filePath, 'r')
    fReaded = f.read()
    f.close()
    return fReaded

while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    req = parserRequest.ParserRequest(request)
    req = req.dictionary()
    data = ''
    
    try:
        data = openFile('.' + req['GET'])
        client_connection.send('HTTP/1.0 200 OK\r\n')
        client_connection.send('Content-Length:' + str(len(data)) + '\r\n')
        client_connection.send('Content-Type: image/jpg\r\n\r\n')
    except IOError:
        httpstatus = httpStatus
        data = httpstatus.TemplateHTTPStatus.forbidden()
        client_connection.send('HTTP/1.0 403 Forbidden\r\n')
        client_connection.send('Content-Length:' + str(len(data)) + '\r\n')
        client_connection.send('Content-Type: text/html\r\n\r\n')
    
    client_connection.send(data)
    client_connection.close()

