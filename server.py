#An HTTP response is made up of the following parts:

#1 The response line a.k.a status line (it's the first line)
#2 Response headers (optional)
#3 A blank line
#4 Response body (optional)

import socket
import os
from _thread import *
import threading
import requests

class TCPServer:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.ThreadCount = 0

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            self.ThreadCount += 1
            start_new_thread(self.thread_clients, (conn, self.ThreadCount,))
            print("Start thread ", self.ThreadCount)
            
            

    def thread_clients(self, connection, _threadCount):
        while True:
            data = connection.recv(1024)
            if not data:
                print("Close thread: ", _threadCount)
                connection.close()
                break
            self.handle_request(data, connection)

    def handle_request(self, data, _conn):
        _conn.sendall(data)

class HTTPServer(TCPServer):
    headers = {
        'Server': 'Base Server',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented'
    }

    def handle_request(self, data, _conn):
        # create an instance of `HTTPRequest`
        request = HTTPRequest(data)

        try:
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            handler = self.HTTP_501_handler

        # now, look at the request method and call the 
        # appropriate handler

        response = handler(request)

        _conn.sendall(response)
    
    def handle_POST(self, request):
        filename = request.uri.strip('/') # remove the slash from the request URI
        content = request.content
        print(content)
        if os.path.exists(filename):
            response_line = self.response_line(status_code=200)

            response_headers = self.response_headers()

            response_body = b"This is respone your POST method.\r\n Params were posted:\r\n"
            response_body = b"".join([response_body, content.decode().replace("&", ",\r\n").replace("=", " : ").encode()])
        else:
            response_line = self.response_line(status_code=404)
            response_headers = self.response_headers()
            response_body = b"<h1>404 Not Found</h1>"

        blank_line = b"\r\n"

        return b"".join([response_line, response_headers, blank_line, response_body])

    def handle_GET(self, request):
        filename = request.uri.strip('/') # remove the slash from the request URI

        if os.path.exists(filename):
            response_line = self.response_line(status_code=200)

            response_headers = self.response_headers()

            '''with open(filename, 'rb') as f:
                response_body = f.read()'''
            response_body = b"This is respone for your GET method"
        else:
            response_line = self.response_line(status_code=404)
            response_headers = self.response_headers()
            response_body = b"<h1>404 Not Found</h1>"

        blank_line = b"\r\n"

        return b"".join([response_line, response_headers, blank_line, response_body])
    
    def HTTP_501_handler(self, request):
        response_line = self.response_line(status_code=501)

        response_headers = self.response_headers()

        blank_line = b"\r\n"

        response_body = b"<h1>501 Not Implemented</h1>"

        return b"".join([response_line, response_headers, blank_line, response_body])

    def response_line(self, status_code):
        reason = self.status_codes[status_code]
        line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)

        return line.encode() # call encode to convert str to bytes
    
    def response_headers(self, extra_headers=None):
        headers_copy = self.headers.copy() # make a local copy of headers

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h, headers_copy[h])

        return headers.encode() # call encode to convert str to bytes

class HTTPRequest:
    def __init__(self, data):
        self.content = ""
        self.method = None
        self.uri = None
        self.http_version = "1.1" # default to HTTP/1.1 if request doesn't provide a version

        self.parse(data)

    def parse(self, data):

        #print(data.split(b"\r\n"))

        lines = data.split(b"\r\n")
        #get method

        request_line = lines[0]
        print(request_line)

        words = request_line.split(b" ")

        self.method = words[0].decode() # call decode to convert bytes to str

        if len(words) > 1:
            # browsers don't send uri for homepage
            self.uri = words[1].decode() # call decode to convert bytes to str

        if len(words) > 2:
            self.http_version = words[2]
        
        #get content
        content = lines[-1]
        self.content = content

if __name__ == '__main__':
    server = HTTPServer()
    server.start()
