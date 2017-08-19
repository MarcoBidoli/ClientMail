#!/usr/bin/env python
# MarcoBidoli

import socket

# Apro un socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Dichiaro la mia classe Funzionitelnet
class Funzionitelnet:
	# creo il costruttore che colleghera il socket al server mail
	def __init__(self, ip, port):
		self.stato = False
		server.connect((ip,port))
		ris = server.recv(1024)

	# metodo che ricevute come parametri due stringhe, esegue il login verso il server di posta
	# e ritorna True o False in base al risultato della connessione
	def login(self, user, password):
		self.stato = False
		server.send("user " + user + "\r\n")
		risp = server.recv(1024)
		if risp == "+OK\r\n":
			self.stato = True
		else:
			self.stato = False
		server.send("pass " + password + "\r\n")
		risp = server.recv(1024)
		if risp == "+OK\r\n":
			self.stato = True
		else:
			self.stato = False
		return self.stato

	def getStatoConnessione(self):
		return self.stato

	# metodo senza parametri che ritorna una stringa contente la lista di mail presenti sul server
	def listaMail(self):
		stringa = ""
		read = True
		server.send("list" + "\r\n")
		while (read == True):
			a = server.recv(1)
			if (a == "."):
				read = False
			stringa = stringa + a
		server.recv(2)
		return stringa

	# metodo utilizzato da "leggiMail" per leggere correttamente tutto il contenuto della mail
	def lr(self,stringa):
		b = stringa.split(" ")
		return b[1]

	# metodo che riceve come parametro un intero e ritorna il contenuto della mail sotto forma di stringa
	def leggiMail(self, n):
		stringa = ""
		server.send("retr " + str(n) + "\r\n")
		dati = server.recv(24)
		server.recv(5)
		limite = self.lr(dati)
		for i in range (0,int(limite)):
			stringa=stringa+server.recv(1)
		return stringa

	# metodo che permette di cancellare una mail sul server di posta, ha come parametro
	# un intero e ritorna True o False in base al successo o meno dell operazione
	def cancellaMail(self, n):
		server.send("dele " + str(n) + "\r\n")
		if server.recv(1024) == "+OK\r\n":
			stato = True
		else:
			stato = False
		return stato

	# metodo che disconette il socket dal server di posta
	def disconnetti(self):
		server.send("quit\r\n")
		server.recv(1024)
		server.close()
		self.stato = False
