import pyqrcode
import os
import wx
from tkfilebrowser import askopenfilename
from profile import Profile


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super(MainWindow, self).__init__()
        self.parent = parent

        self.png = pyqrcode.QRCode
        self.bitmap = wx.StaticBitmap
        self.qrprofile = Profile

        topsizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        wx.Frame.__init__(self, parent, wx.ID_ANY, title=title, size=(250, 300))
        self.control = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.label = wx.StaticText(self, wx.ID_ANY, style=wx.TE_CENTER)
        self.label.SetBackgroundColour("white")
        self.resetIdList = wx.Button(self, wx.ID_ANY, "ID-Liste zurücksetzen")
        self.loadQR = wx.Button(self, wx.ID_ANY, "QR-Code prüfen")

        topsizer.Add(self.control, 1, wx.ALIGN_CENTER)
        topsizer.Add(self.label, 1, wx.ALIGN_CENTER)
        # StaticText um DateOfPurchase zu zeigen
        button_sizer.Add(self.resetIdList, 0, wx.ALL, 10)
        topsizer.Add(button_sizer, wx.SizerFlags(0).Center())
        self.SetSizerAndFit(topsizer)
        self.CreateStatusBar()

        #  Verknüpfen der Buttons mit Funktionen
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter, self.control)
        self.Bind(wx.EVT_BUTTON, self.onClickedReset, self.resetIdList)
        self.Bind(wx.EVT_BUTTON, self.onClickedLoadQR, self.loadQR)

        self.Show(True)

    #  Event beim klicken des Laden-Buttons: lade QRCode.png
    def onClickedLoadQR(self, e):
        file_path = askopenfilename(initialdir="C:\\", initialfile="tmp",
                                    filetypes=[("Pictures", "*.png"), ("All Files", "*")])
        print(file_path)
        self.png = wx.Image(file_path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(self, wx.ID_ANY, self.png, (10, 5),
                                      (self.png.GetWidth(), self.png.GetHeight()))
        self.Update()

    # Event beim klicken des Löschen-Buttons: instanz des Objekts löschen
    def onClickedDelete(self, e):
        del self.qrprofile

    # Event beim klicken des Reset-Buttons: idList.txt zurücksetzen
    def onClickedReset(self, e):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.remove(dir_path + '\\idList.txt')
        with open("idList.txt", "w") as reset_list:
            reset_list.write("")

    #  Event beim Drücken der Enter-Taste: Instanz des Objekts profile erzeugen und QRCode generieren und .png erstellen
    def onEnter(self, e):
        name = str(self.control.GetValue())
        self.qrprofile = Profile(name)
        self.png = wx.Image(self.qrprofile.getFileName(), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(self, wx.ID_ANY, self.png, (10, 5), (150, 150))
        self.bitmap.SetPosition((0, 50))
        self.Update()


def main():
    app = wx.App(False)
    frame = MainWindow(None, "QRCode Ticketautomat")
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
