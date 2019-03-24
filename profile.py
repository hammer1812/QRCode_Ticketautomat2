import pyqrcode
import random
from datetime import datetime


class Profile:
    name = " "
    id = 0
    dateOfPurchase = " "
    price = 0
    idList = []
    stringID = " "
    idQR = pyqrcode.QRCode
    fileName = " "

    #  Initialisierung des Objekts
    def __init__(self, name):
        self.name = name
        self.dateOfPurchase = datetime.now()
        self.__generateID()
        self.price = 35
        #  Preis berechnen und abhängig von dateOfPurchase machen

    def __del__(self):  # I'm about to end this man's whole career.
        del self.name
        del self.id
        del self.dateOfPurchase
        del self.price
        del self.idList
        del self.stringID
        del self.idQR

    #  private Methode zum erzeugen der ID und des QRCOdes
    def __generateID(self):
        self.id = random.randrange(10000, 99999, 1)
        with open("idList.txt", "r") as read_list:
            read_list.seek(0)
            self.idList = read_list.readlines()
            while self.id not in self.idList:
                self.idList.append(self.id)
                self.stringID += self.name[0]
                self.stringID += str(datetime.now())
                self.stringID += str(self.id)
                self.stringID += self.name[-1]
                self.fileName = ("QRCode" + self.name + ".png")
                with open("idList.txt", "w") as write_list:
                    #  write_list.writelines(str(self.id) + "\n")
                    for idNumber in self.idList:
                        if idNumber != ';':
                            write_list.write("%s;" % idNumber)
                self.idQR = pyqrcode.create(str(self.id) + "\n" + self.name + "\n" + str(self.dateOfPurchase), error='L', mode='binary')
                self.idQR.png(self.fileName, scale=5)

    #  die "verschlüsselte" ID in Form eines Strings
    def getStringID(self):
        return self.stringID

    #  die ID, wie sie in idList gespeichert ist
    def getID(self):
        return self.id

    #  der korrespondierende Name
    def getName(self):
        return self.name

    #  das korrespondierende Kaufdatum
    def getDateOfPurchase(self):
        return self.dateOfPurchase

    #  das korrespondierende QRCode-Objekt
    def getQRImage(self):
        return self.idQR

#  Dateiname des QRCodes
    def getFileName(self):
        return self.fileName
