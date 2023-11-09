
from random import shuffle

#Loob kaardid ühe kaardipaki jaoks
mastid = ("Ruu", "Ärt", "Pot", "Ris")
ühikud = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
kaardid = tuple(mast + ühik for mast in mastid for ühik in ühikud)

#Määrab igale kaardile väärtuse
väärtused = (2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10) * 4 #4 erinevat masti, 10, J, Q, K, A sama väärtusega
KaardiVäärtus = {kaart: väärtus for kaart, väärtus in zip(kaardid, väärtused)}

#Segab kaardipaki ära
PakiKogus = 4 #Mitu kaardipakki korraga kasutuses
kaardipakk = PakiKogus * list(kaardid)
shuffle(kaardipakk)