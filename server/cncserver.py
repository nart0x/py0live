import time
import os
import socket
import threading
import SocketServer
import uuid

VERSION = '0.1'

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

	

	def handle(self):
		data = self.request.recv(1024)
		cur_thread = threading.current_thread()
		self.processData(data)


	def processData(self, data):

		print 'Got:', data

		client_time = data.split(":")[0]
		client_id = data.split(":")[1]
		client_build = data.split(":")[2]
		client_server_id_flag = data.split(":")[3]
		client_status = data.split(":")[4]

		if client_status == "50":
			# request more information from the client     
			self.client_HANDSHAKE()
		elif client_status == "100":
			self.client_HEARTBEAT()
		else: 
			self.request.sendall(self.protocolFromat('1','0'))

		#print "Bot_time = %s\nBot_id = %s\nBot_build = %s\nBot_data = %s\n" %(bot_time,bot_id,bot_build,bot_data)
		return 0 

	def client_HEARTBEAT(self):
		self.request.sendall(self.protocolFromat('1','0'))

	def client_HANDSHAKE(self):
		self.request.sendall(self.protocolFromat('1','0'))

	def protocolFromat(self, status, data):
		# See py0live_protocol_documentation.txt
		global VERSION
		protocol = "%s:%s:%s:%s:%s:%s" % (self.timeNow(), self.getID(), VERSION, 0, status, data)
		return str(protocol)

	def timeNow(self):
		return int(round(time.time() * 1000))

	def getID(self):

		if os.path.isfile("IDF"):
			f = open("IDF", 'r')
			reading = f.readline()
			return str(reading)
		else:
			f = open("IDF", 'w')
			ident = uuid.uuid4()
			f.write(str(ident))
			return str(ident)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == "__main__":
	# Port 0 means to select an arbitrary unused port
	HOST, PORT = "127.0.0.1", 4069

	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	ip, port = server.server_address

	# Start a thread with the server -- that thread will then start one
	# more thread for each request
	server_thread = threading.Thread(target=server.serve_forever)
	# Exit the server thread when the main thread terminates
	server_thread.daemon = True
	server_thread.start()
	print "Server loop running in thread:", server_thread.name

	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print 'KeyboardInterrupt'
		server.shutdown()
		server.server_close()
	except: 
		server.shutdown()
		server.server_close()