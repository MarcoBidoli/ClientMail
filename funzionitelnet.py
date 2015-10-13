#!/usr/bin/env python
import socket

# Apro un socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Dichiaro la mia classe Funzionitelnet
class Funzionitelnet:
	# creo il costruttore che colleghera il socket al server mail
	def __init__(self, ip, port):
		server.connect((ip,port))
		ris = server.recv(1024)
	
	# metodo che ricevute come parametri due stringhe, esegue il login verso il server di posta
	# e ritorna True o False in base al risultato della connessione	
	def login(self, user, password):
		stato = False
		server.send("user " + user + "\r\n")
		risp = server.recv(1024)
		if risp == "+OK\r\n":
			stato = True
		else:
			stato = False
		server.send("pass " + password + "\r\n")
		risp = server.recv(1024)
		if risp == "+OK\r\n":
			stato = True
		else:
			stato = False
		return stato
	
	# metodo senza parametri che ritorna una stringa contente la lista di mail presenti sul server	
	def listaMail(self):
		server.send("list" + "\r\n")
		return server.recv(4096)
	
	# metodo utilizzato da "leggiMail" per leggere correttamente tutto il contenuto della mail		
	def lr(self,stringa):
		b = stringa.split(" ")
		return b[1]		
		return stringa
		
	# metodo che riceve come parametro un intero e ritorna il contenuto della mail sotto forma di stringa
	def leggiMail(self, n):
		stringa=""
		server.send("retr " + str(n) + "\r\n")
		limite = self.lr(server.recv(24))
		print limite
		for i in range (0,int(limite)):
			stringa=stringa+server.recv(1)
		return stringa
		
	# metodo che permette di cancellare una mail sul server di posta, ha come parametro
	# un intero e ritorna True o False in base al successo o meno dell operazione 
	def cancellaMail(self, n):
		server.send("dele " + n + "\r\n")
		if server.recv(1024) == "+OK\r\n":
			stato = True
		else:
			stato = False
		return stato
		
	# metodo che disconette il socket dal server di posta
	def disconnetti(self):
		server.send("quit")	
