
from random import shuffle, randint

#Loob kaardid ühe kaardipaki jaoks
mastid = ("Ruu", "Ärt", "Pot", "Ris")
ühikud = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
kaardid = tuple(mast + ühik for mast in mastid for ühik in ühikud)

#Määrab igale kaardile väärtuse
väärtused = (2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11) * 4 #4 erinevat masti, 10, J, Q, K sama väärtusega, A on praegu 11
KaardiVäärtus = {kaart: väärtus for kaart, väärtus in zip(kaardid, väärtused)}

#----------------
#Ma pole kindel, kui suur osa programmist peaks olema funktsioonides ning kui palju võib niisama olla, võid vabalt võtta funktsioonidest välja kui soovid

kaardipakk = [] #Tühi muutuja, mida kasutatakse kaardipakina
PakiKogus = 4 #Mitu kaardipakki korraga kasutuses on?
KaardiHulk = 0
#Segab kaardipaki ära
def sega():
    global kaardipakk
    global PakiKogus
    global KaardiHulk
    kaardipakk = PakiKogus * list(kaardid)
    shuffle(kaardipakk)
    KaardiHulk = PakiKogus * 52

#Kaardi kaardipakist võtmisfunktsioon
def hit():
    global kaardipakk
    global KaardiHulk
    if KaardiHulk == 0: sega()
    KaardiHulk -= 1
    return kaardipakk.pop(0)