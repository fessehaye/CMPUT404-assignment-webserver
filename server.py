import SocketServer, os.path
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
	new_path = self.data.split(" ")[1]
	
	if (new_path[-1] == "/"):
		new_path += "index.html"

	new_path = "www" + os.path.normpath(new_path)
	content = ""
	header = "HTTP/1.1 "
	try:
		extension = os.path.splitext(new_path)[1]
		extension = extension[1:]
		path_file = open(new_path,"r")

		with path_file as filedata:
			content = filedata.read()

		header += "200\n"
		header += "Content-Type: text/" + extension + "\n"
	except IOError:
		header += "404\n"

	self.request.sendall(header + "\n" + content)
	
	

	
	
		

        #print ("Got a request of: %s\n" % new_path)
	
        #self.request.sendall("OK")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
