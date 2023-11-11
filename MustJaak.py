
from random import shuffle, randint


class Kaardipakk:
    # Uus segatud kaardipakk (klassi välja kutsumisel)
    def __init__(self, pakikogus):
        # Loob kaardid ühe kaardipaki jaoks
        mastid = ("Ruu", "Ärt", "Pot", "Ris")
        ühikud = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
        üks_pakk = [mast + ühik for mast in mastid for ühik in ühikud]

        # Määrab igale kaardile väärtuse
        väärtused = (2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11) * 4  # 4 erinevat masti, 10, J, Q, K sama väärtusega
        self.KaardiVäärtus = {kaart: väärtus for kaart, väärtus in zip(üks_pakk, väärtused)}

        # Määratud pikkusega kaardipakk, segab paki ära
        self.kaardipakk = pakikogus * üks_pakk
        shuffle(self.kaardipakk)
        self.kaardihulk = pakikogus * 52  # Kaartide kogus, et ei peaks koguaeg len()-i välja kutsuma
        self.vahekaart = randint(round(self.kaardihulk * 0.4), round(self.kaardihulk * 0.6))  # Millal uuesti segatakse?

    # Kaardipakist võetakse uus kaart
    def hit(self):
        self.kaardihulk -= 1
        kaart = self.kaardipakk.pop(0)
        return kaart, self.KaardiVäärtus[kaart]


class Mängija:
    def __init__(self, nimi):
        self.nimi = nimi
        self.kaardid = []
        self.väärtus = 0
        self.A11 = 0

    def uuskaart(self, kaart, väärtus):
        self.kaardid.append(kaart)
        self.väärtus += väärtus

        self.A11 += 1 if kaart[3:] == "A" else 0
        if self.väärtus > 21 and self.A11 > 0:
            self.väärtus -= 10
            self.A11 -= 1


# Mängijate määramine
MängijadArv = 4  # Mitu mängijat mängu mängib
MängijaKoht = 2  # Mitmes koht on pärismängijal

MängijaNimed = ["Diiler"] + ["Arvuti" + str(i) for i in range(1, MängijadArv)]
MängijaNimed.insert(MängijaKoht, "Mängija")

mängijad = {nimi: Mängija(nimi) for nimi in MängijaNimed}
kaardid = Kaardipakk(4)

