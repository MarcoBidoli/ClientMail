#!/usr/bin/env python
# MarcoBidoli

import funzionitelnet
import os

ip = "mail.plazzotta.eu"
port = 110
account = funzionitelnet.Funzionitelnet(ip,port)

n = 999
while n != '0':
	os.system("clear")
	print "1. Log-in"
	print "2. List"
	print "3. Mail"
	print "4. Cancella"
	print "0. Logout"
	n = raw_input("-> ")

	if n == '1':
		if account.getStatoConnessione() == False:
			usr = raw_input("E-mail: ")
			passwd = raw_input("Password: ")
			#usr = "test2@plazzotta.eu"
			#passwd = "ArcilesiCanci"
			risp = account.login(usr, passwd)
			if risp == True:
				print "Connesso"
			else:
				print "ERRORE"
		else:
			print "Sei gia connesso"
		raw_input("Premi invio..")

	elif n == '2':
		if account.getStatoConnessione() == True:
			print account.listaMail()
		else:
			print "Non sei connesso"
		raw_input("Premi invio..")

	elif n == '3':
		if account.getStatoConnessione() == True:
			a = raw_input("Numero mail: ")
			print account.leggiMail(a)
		else:
			print "Non sei connesso"
		raw_input("Premi invio..")

	elif n == '4':
		if account.getStatoConnessione() == True:
			a = raw_input("Numero mail: ")
			if account.cancellaMail(a) == True:
				print "Cancellata"
			else:
				print "Errore"
		else:
			print "Non sei connesso"
		raw_input("Premi invio..")

	else:
		if account.getStatoConnessione() == True:
			print "Disconnesso"
			account.disconnetti()
