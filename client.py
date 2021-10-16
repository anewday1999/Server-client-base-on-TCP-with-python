#An HTTP request is made up of the following parts:

#1 The request line (it's the first line) {Method Link HTTPVersion LineBreak}
#2 Request headers (optional)
#3 A blank line
#4 Request body (optional)

'''import requests
from _thread import *
import threading

def get_method():
    url = "http://127.0.0.1:8000/index.html"
    response = requests.get(url)
    print(response.content.decode())

def post_method():
    data = {"key1": "1", "key2" : "2"}
    url = "http://127.0.0.1:8000/index.html"
    response = requests.post(url, data)
    print(response.content.decode())

#get_method()
post_method()'''


# Import socket module
import socket
from _thread import *
import threading
import time
  
  
class Client():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
  
    # Define the port on which you want to connect
    port = 8000
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  
    # connect to server on local computer
    s.connect((host,port))
    
    def get_method(self):
        while True:
            request = "GET /index.html HTTP/1.1"
            # message sent to server
            self.s.send(request.encode('ascii'))

            # messaga received from server
            data = self.s.recv(1024)

            # print the received message
            # here it would be a reverse of sent message
            print(str(data.decode('ascii')).split("\n")[-1])
            c = input("=======1-GET=========0-EXIT===========")
            if c == "1":
                continue
            else:
                break


    def post_method(self):
        while True:
            headers = """POST /index.html HTTP/1.1\r
            Content-Type: {content_type}\r
            Content-Length: {content_length}\r
            Host: {host}\r
            Connection: close\r
            \r\n"""

            body = 'key1=1&key2=2'                                 
            body_bytes = body.encode('ascii')
            header_bytes = headers.format(
                content_type="application/x-www-form-urlencoded",
                content_length=len(body_bytes),
                host=str(self.host) + ":" + str(self.port)
            ).encode('iso-8859-1')

            payload = header_bytes + body_bytes

            self.s.send(payload)
            data = self.s.recv(1024)
            count = 0
            for line in str(data.decode('ascii')).split("\n"):
                count += 1
                if count >= 4:
                    print(line)
            c = input("=======1-POST=========0-EXIT===========")
            if c == "1":
                continue
            else:
                break

    def close_socket(self):
        self.s.close()
  
if __name__ == '__main__':
    client = Client()
    client.post_method()
    client.close_socket()