#! /usr/bin/env python

import wx
import funzionitelnet

class Finestra(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, pos=(10,10), size=(700,420))
		
		self.account = funzionitelnet.Funzionitelnet("mail.plazzotta.eu", 110)
				
		self.pannello = wx.Panel(self, -1)
		#barra dei menu
		self.menu = wx.MenuBar()
		# aggancio al panel
		self.SetMenuBar(self.menu)
		
		#creo menu e aggancio voci
		self.menu1 = wx.Menu()
		self.menu1.Append(10, "Login", "Collegati al server")
		self.menu1.Append(11, "Logout e Esci","Chiudi il programma")
		
		self.menu.Append(self.menu1, "File..")
		self.Bind(wx.EVT_MENU, self.ascoltatore)
		
		#listbox
		self.listBox = wx.ListBox(self.pannello, 200, pos=(10,10), size=(100,350))
		self.listBox.Bind(wx.EVT_LISTBOX, self.ascoltaListBox)
		
		#textctrl
		self.oggettoCtrl = wx.TextCtrl(self.pannello, 300, pos=(130, 10), size=(460,-1))
		self.testoCtrl = wx.TextCtrl(self.pannello, 301, pos=(130, 50), size=(460, 310), style=wx.TE_MULTILINE)
		
		#button
		refresh = wx.BitmapButton(self.pannello, 400, wx.Bitmap("images/refresh.png"), pos=(610, 80), size=(60,60))
		cestino = wx.BitmapButton(self.pannello, 401, wx.Bitmap("images/bin.png"), pos=(610, 180), size=(60,60))
		self.Bind(wx.EVT_BUTTON, self.ascoltatore)
	
	def ascoltatore(self, evt):
		premuto = evt.GetId()
		
		#menu
		if premuto == 10:
			if self.account.getStatoConnessione() == False:
				l = Login(None, self.account, -1, "Login")
				l.Show()
			else:
				wx.MessageBox("Hai gia effetuato il login")
		if premuto == 11:
			if self.account.getStatoConnessione() == True:
				self.account.disconnetti()
			self.Close()

		#button
		if premuto == 400:
			if self.account.getStatoConnessione() == True:
				self.aggiorna()
			else:
				wx.MessageBox("Non hai ancora effetuato il login")
		
		if premuto == 401:
			if self.account.getStatoConnessione() == True:
				self.elimina()
			else:
				wx.MessageBox("Non hai ancora effetuato il login")
	
	def ascoltaListBox(self,evt):
		if self.account.getStatoConnessione() == True:
			n = self.listBox.GetSelection()
			nMail = self.lista_mail[n].split(" ")[0]
			self.oggettoCtrl.SetValue("Mail " + str(nMail))
			testo = self.account.leggiMail(nMail)
			self.testoCtrl.SetValue(testo)

	def aggiorna(self):
		self.lista_mail = []
		stringa = self.account.listaMail()
		listaTmp = stringa.split("\r\n")
		listaTmp.pop(0)
		listaTmp.pop(len(listaTmp)-1)
		for el in listaTmp:
			tmp = el.split(" ")
			self.lista_mail.append(el)
		self.listBox.Set(self.lista_mail)
	
	def elimina(self):
		el = self.listBox.GetSelection()
		n = self.lista_mail[el].split(" ")[0]
		print "Cancello " + str(n)
		check = self.account.cancellaMail(n)
		if check == True:
			wx.MessageBox("Mail eliminata", "Info")
		else:
			wx.MessageBox("Errore non specificato", "Error")
		self.aggiorna()

class Login(wx.Frame):
	def __init__(self, parent, oggetto, id, title):
		wx.Frame.__init__(self, parent, id, title, pos=(50,50), size=(200,250))
		
		self.oggetto = oggetto
		self.pannello = wx.Panel(self, -1)
		
		self.user_text = wx.TextCtrl(self.pannello, 201, pos=(20,50), size=(150,-1))
		self.pass_text = wx.TextCtrl(self.pannello, 202, pos=(20,130), size=(150,-1), style=wx.TE_PASSWORD)
		self.user_label = wx.StaticText(self.pannello, 301, "Mail", pos=(20, 20), size=(200,30))
		self.pass_label = wx.StaticText(self.pannello, 302, "Pasword", pos=(20, 100), size=(200,30))
		self.login_button = wx.Button(self.pannello, 101, label='Login', pos=(40,180), size=(100,40))
		
		self.Bind(wx.EVT_BUTTON,self.controlla)
		
	def controlla(self, evt):
		id_button = evt.GetId()
		if id_button == 101:
			user = self.user_text.GetValue()
			passwd = self.pass_text.GetValue()
			check = self.oggetto.login(user,passwd)
			if check == True:
				wx.MessageBox("Connesso")
				self.Close()
			else:
				wx.MessageBox("Email o password errati")			
# Avvio il programma
a = wx.App()
f = Finestra(None, -1, "Client Mail")
f.Show(True)
a.MainLoop()
