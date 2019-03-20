import pyqrcode
import time
import random
import os
import wx
import sys
import traceback
import tkinter
from tkfilebrowser import askopendirname, askopenfilename, asksaveasfilename


class Panels(wx.Panel):
	def __init__(self, parent, id):
		wx.Panel.__init__(self, parent)
		self.parent = parent

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		super(MainWindow, self).__init__()
		self.parent = parent

		# self.panel = wx.Panel(self)
		#
		# self.vsizer = wx.BoxSizer(wx.VERTICAL)
		# self.nm = wx.StaticBox(self.panel, wx.ID_ANY, "Name: ")
		# self.nmSizer = wx.StaticBoxSizer(self.nm, wx.VERTICAL)
		# self.hsizer = wx.BoxSizer(wx.HORIZONTAL)

		topsizer = wx.BoxSizer(wx.VERTICAL)
		button_sizer = wx.BoxSizer(wx.HORIZONTAL)

		wx.Frame.__init__(self, parent, wx.ID_ANY, title=title, size=(250, 300))
		self.control = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
		self.label = wx.StaticText(self, wx.ID_ANY, style=wx.TE_CENTER)
		self.label.SetBackgroundColour("white")
		self.resetIdList = wx.Button(self, wx.ID_ANY, "ID-Liste zurücksetzen")
		self.loadQR = wx.Button(self, wx.ID_ANY, "QR-Code prüfen")
		#self.resetIdList.SetPosition((500, 0))

		topsizer.Add(self.control, 1, wx.EXPAND)
		# StaticText um DateOfPurchase zu zeigen
		button_sizer.Add(self.resetIdList, 0, wx.ALL, 10)
		topsizer.Add(button_sizer, wx.SizerFlags(0).Center())
		self.SetSizerAndFit(topsizer)


		# self.vsizer.Add(self.control, 0, 0, 0)
		# self.vsizer.Add(self.label, 0, 0, 0)
		# self.hsizer.Add(self.resetIdList, 0, wx.ALIGN_RIGHT)
		# self.nmSizer.Add(self.vsizer, 0, 0, 0)
		# self.panel.SetSizer(self.vsizer)
		self.CreateStatusBar()

		self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter, self.control)
		self.Bind(wx.EVT_BUTTON, self.OnClickedReset, self.resetIdList)
		self.Bind(wx.EVT_BUTTON, self.onClickedLoadQR, self.loadQR)

		self.Show(True)

	def onClickedLoadQR(self, e):
		file_path = askopenfilename(initialdir="C:\\", initialfile="tmp", filetypes=[("Pictures", "*.png"), ("All Files", "*")])
		print(file_path)
		with open(file_path) as load_code:
			self.png = wx.Image(file_path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
			self.bitmap = wx.StaticBitmap(self, wx.ID_ANY, self.png, (10, 5), (self.png.GetWidth(), self.png.GetHeight()))
			self.Update()

	def OnClickedReset(self, e):# Event beim klicken des Reset-Buttons
		dir_path = os.path.dirname(os.path.realpath(__file__))
		os.remove(dir_path + '\\idList.txt')
		with open("idList.txt", "w") as reset_list:
			reset_list.write("")



	def OnEnter(self, e):	#Event beim Drücken der Enter-Taste
		name = str(self.control.GetValue())
		self.label.SetLabel(generateID(name))
		self.png = wx.Image("QRCode" + name + ".png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		self.bitmap = wx.StaticBitmap(self, -1, self.png, (10, 5), (self.png.GetWidth(), self.png.GetHeight()))
		self.bitmap.SetPosition((0, 50))
		self.Update()


def generateID(name):
	stringID = ""
	id = random.randrange(10000, 99999, 1)
	with open("idList.txt", "r") as read_list:
		read_list.seek(0)
		idList = read_list.readlines()
		while id not in idList:
			idList.append(id)
			stringID += name[0]
			stringID += time.strftime("%d%m%y%H%M")
			stringID += str(id)
			stringID += name[-1]
			with open("idList.txt", "w") as write_list:
				write_list.writelines("%s\n" % line for line in idList)
			idQR = pyqrcode.create(str(id) + "\n" + name + "\n" + time.strftime("%d%m%y%H%M"), error='L', mode='binary')
			idQR.png('QRCode' + name + '.png', scale=5)
			return stringID
	return None


def main():
	app = wx.App(False)
	frame = MainWindow(None, "QRCode Ticketautomat")
	frame.Show()
	app.MainLoop()


if __name__ == '__main__':
	main()