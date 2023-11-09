
from random import shuffle, randint

#Loob kaardid ühe kaardipaki jaoks
mastid = ("Ruu", "Ärt", "Pot", "Ris")
ühikud = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
kaardid = tuple(mast + ühik for mast in mastid for ühik in ühikud)

#Määrab igale kaardile väärtuse
väärtused = (2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10) * 4 #4 erinevat masti, 10, J, Q, K, A sama väärtusega
KaardiVäärtus = {kaart: väärtus for kaart, väärtus in zip(kaardid, väärtused)}

#----------------
#Ma pole kindel, kui suur osa programmist peaks olema funktsioonides ning kui palju võib niisama olla, võid vabalt võtta funktsioonidest välja kui soovid

kaardipakk = [] #Tühi muutuja, mida kasutatakse kaardipakina
PakiKogus = 4 #Mitu kaardipakki korraga kasutuses on?

#Segab kaardipaki ära
def sega():
    global kaardipakk
    global PakiKogus
    kaardipakk = PakiKogus * list(kaardid)
    shuffle(kaardipakk)

#Kaardi kaardipakist võtmisfunktsioon
def hit():
    global kaardipakk
    return kaardipakk.pop(0)
