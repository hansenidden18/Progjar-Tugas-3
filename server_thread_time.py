from socket import *
import socket
import threading
import logging
import time
import sys

class ProcessTheClient(threading.Thread):
	def __init__(self,connection,address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		msg=""
		while True:
			data = self.connection.recv(32)
			if data:
				d = data.decode()
				msg = msg+d
				print(msg[-2:], msg[:4])
				if msg[-2:] == '\r\n' and msg[:4] == 'TIME':
					curr_time = time.strftime("%H:%M:%S")
					hasil = f"JAM {curr_time}\r\n"
					logging.warning(f"[SERVER] balas ke cliend: {hasil}")
					hasil = hasil.encode()
					self.connection.sendall(hasil)
					msg=""
				else:
					break
			else:
				break
		self.connection.close()

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0',45000))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"connection from {self.client_address}")
			
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()


