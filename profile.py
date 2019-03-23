import pyqrcode
import random
from cryptography.fernet import Fernet
from datetime import datetime


class Profile:
    name = " "
    id = 0
    dateOfPurchase = " "
    price = 0
    idList = []
    stringID = " "
    idQR = pyqrcode.QRCode
    key = Fernet
    encryption = Fernet

    #  Initialisierung des Objekts
    def __init__(self, name):
        self.name = name
        self.dateOfPurchase = datetime.now()
        self.__generateID()
        self.key = Fernet.generate_key()
        self.encryption = Fernet(self.__key)

    def __del__(self):  # I'm about to end this man's whole career.
        del self.name
        del self.id
        del self.dateOfPurchase
        del self.price
        del self.idList
        del self.stringID
        del self.idQR
        del self.key

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
                self.stringID += str(id)
                self.stringID += self.name[-1]
                with open("idList.txt", "w") as write_list:
                    #  write_list.writelines(self.encryption.encrypt(b"%s") % line for line in self.idList)
                    entry = self.encryption.encrypt("%d".encode(), self.id)
                    write_list.write(entry)
                self.idQR = pyqrcode.create(str(self.id) + "\n" + self.name + "\n" + self.dateOfPurchase, error='L', mode='binary')
                self.idQR.png('QRCode' + self.name + '.png', scale=5)

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
