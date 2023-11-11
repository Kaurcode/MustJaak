
from random import shuffle, randint


class Kaardipakk:
    # Uus segatud kaardipakk (klassi välja kutsumisel)
    def __init__(self, pakikogus):
        # Muutuja kaardi tähistamiseks
        self.kaart = None

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
        self.kaart = self.kaardipakk.pop(0)
        return self.kaart, self.KaardiVäärtus[self.kaart]


class Mängija:
    def __init__(self, nimi):
        self.nimi = nimi
        self.kaardid = []
        self.väärtus = 0
        self.A11 = 0
        self.kaardidarv = 0
        self.luba_double = 0
        self.luba_split = 0
        self.kaardiväärtus = 0

    def uuskaart(self, kaartväärtus):
        kaart, self.kaardiväärtus = kaartväärtus
        self.kaardid.append(kaart)
        self.väärtus += self.kaardiväärtus
        self.kaardidarv += 1
        self.luba_double = 1 if self.kaardidarv == 2 else 0
        self.luba_split = 1 if self.kaardidarv == 2 and self.kaardid[0][3:] == self.kaardid[1][3:] else 0

        self.A11 += 1 if kaart[3:] == "A" else 0
        if self.väärtus > 21 and self.A11 > 0:
            self.väärtus -= 10
            self.A11 -= 1

    def split(self):
        self.väärtus -= self.kaardiväärtus
        self.kaardidarv -= 1
        return self.kaardid.pop(), self.kaardiväärtus


# Olenevalt kaartidest väljastab funktsioon parima valiku
# Blackjacki basic strateegia võtsin Blackjacki Wikipeedia saidilt: https://en.wikipedia.org/wiki/Blackjack
# S = Stand; H = Hit; Dh = Double/Hit; Ds = Double/Stand; SP = Split
# Uh = Surrender/hit; Us = Surrender/stand; Usp = Surrender/split
def strateegia(väärtus, kaardid, diiler):
    paar = len(kaardid) == 2  # Kas on kaks kaarti?
    pildikaart = ("J", "Q", "K")
    kaardid_pildita = ["10" if kaart[3:] in pildikaart else kaart[3:] for kaart in kaardid]  # Pildikaart = "10"

    # Diileri nähtava kaardi asukoht tabelis
    diilervõimalik = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "A")
    diiler = "10" if diiler in pildikaart else diiler
    diilerindeks = diilervõimalik.index(diiler)

    # Paar (2 sama kaarti)
    if paar and kaardid_pildita[0] == kaardid_pildita[1]:
        paar = ("A", "10", "9", "8", "7", "6", "5", "4", "3", "2")
        kaartindeks = paar.index(kaardid_pildita[0])
        # Diiler:  2     3     4     5     6     7     8     9     10    A
        tabel = (("SP", "SP", "SP", "SP", "SP", "SP", "SP", "SP", "SP", "SP"),  # A,A
                 ("S", "S", "S", "S", "S", "S", "S", "S", "S", "S"),  # 10,10
                 ("SP", "SP", "SP", "SP", "SP", "S", "SP", "SP", "S", "S"),  # 9,9
                 ("S", "S", "S", "S", "S", "S", "S", "S", "S", "Usp"),  # 8,8
                 ("SP", "SP", "SP", "SP", "SP", "SP", "H", "H", "H", "H"),  # 7,7
                 ("SP", "SP", "SP", "SP", "SP", "H", "H", "H", "H", "H"),  # 6,6
                 ("Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "H", "H"),  # 5,5
                 ("H", "H", "H", "SP", "SP", "H", "H", "H", "H", "H"),  # 4,4
                 ("SP", "SP", "SP", "SP", "SP", "SP", "H", "H", "H", "H"),  # 3,3
                 ("SP", "SP", "SP", "SP", "SP", "SP", "H", "H", "H", "H"))  # 2,2
        return tabel[kaartindeks][diilerindeks]

    # "Soft totals" - Pehme väärtus (kaartide seas esineb äss)
    elif paar and "A" in kaardid_pildita:
        kaardid_pildita.pop(kaardid_pildita.index("A"))
        kaart = int(kaardid_pildita[0])
        teinekaart = tuple(range(10, 1, -1))
        kaartindeks = teinekaart.index(kaart)
        # Diiler:  2    3    4    5    6    7    8    9    10   A
        tabel = (("S", "S", "S", "S", "S", "S", "S", "S", "S", "S"),  # A,10
                 ("S", "S", "S", "S", "S", "S", "S", "S", "S", "S"),  # A,9
                 ("S", "S", "S", "S", "Ds", "S", "S", "S", "S", "S"),  # A,8
                 ("Ds", "Ds", "Ds", "Ds", "Ds", "S", "S", "H", "H", "H"),  # A,7
                 ("H", "Ds", "Ds", "Ds", "Ds", "H", "H", "H", "H", "H"),  # A,6
                 ("H", "H", "Ds", "Ds", "Ds", "H", "H", "H", "H", "H"),  # A,4-A,5 (A,5)
                 ("H", "H", "Ds", "Ds", "Ds", "H", "H", "H", "H", "H"),  # A,4-A,5 (A,4)
                 ("H", "H", "H", "Ds", "Ds", "H", "H", "H", "H", "H"),  # A,2-A,3 (A,3)
                 ("H", "H", "H", "Ds", "Ds", "H", "H", "H", "H", "H"))  # A,2-A,3 (A,2)
        return tabel[kaartindeks][diilerindeks]

    # "Hard totals" - kõik muu, ehk arvestatakse kaartide väärtuse järgi
    else:
        väärtused = tuple(range(21, 4, -1))
        väärtus = int(väärtus)
        väärtusindeks = väärtused.index(väärtus)
        # Diiler:  2    3    4    5    6    7    8    9    10   A
        tabel = (("S", "S", "S", "S", "S", "S", "S", "S", "S", "S"),  # 18-21 (21)
                 ("S", "S", "S", "S", "S", "S", "S", "S", "S", "S"),  # 18-21 (20)
                 ("S", "S", "S", "S", "S", "S", "S", "S", "S", "S"),  # 18-21 (19)
                 ("S", "S", "S", "S", "S", "S", "S", "S", "S", "S"),  # 18-21 (18)
                 ("S", "S", "S", "S", "S", "S", "S", "S", "S", "Us"),  # 17
                 ("S", "S", "S", "S", "S", "H", "H", "Uh", "Uh", "Uh"),  # 16
                 ("S", "S", "S", "S", "S", "H", "H", "H", "Uh", "Uh"),  # 15
                 ("S", "S", "S", "S", "S", "H", "H", "H", "H", "H"),  # 13-14 (14)
                 ("S", "S", "S", "S", "S", "H", "H", "H", "H", "H"),  # 13-14 (13)
                 ("H", "H", "S", "S", "S", "H", "H", "H", "H", "H"),  # 12
                 ("Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "Dh"),  # 11
                 ("Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "H", "H"),  # 10
                 ("H", "Dh", "Dh", "Dh", "Dh", "H", "H", "H", "H", "H"),  # 9
                 ("H", "H", "H", "H", "H", "H", "H", "H", "H", "H"),  # 5-8 (8)
                 ("H", "H", "H", "H", "H", "H", "H", "H", "H", "H"),  # 5-8 (7)
                 ("H", "H", "H", "H", "H", "H", "H", "H", "H", "H"),  # 5-8 (6)
                 ("H", "H", "H", "H", "H", "H", "H", "H", "H", "H"))  # 5-8 (5)
        return tabel[väärtusindeks][diilerindeks]


# Mängijate määramine
MängijadArv = 4  # Mitu mängijat mängu mängib
MängijaKoht = 2  # Mitmes koht on pärismängijal

MängijaNimed = ["Diiler"] + ["Arvuti" + str(i) for i in range(1, MängijadArv)]
MängijaNimed.insert(MängijaKoht, "Mängija")

mängijad = {nimi: Mängija(nimi) for nimi in MängijaNimed}

# Mäng
kaardipakk = Kaardipakk(4)  # Uus kaardipakk
# Diiler
mängijad["Diiler"].uuskaart(kaardipakk.hit())  # Nähtav kaart
print(kaardipakk.kaart)
print(mängijad["Diiler"].väärtus)
mängijad["Diiler"].uuskaart(kaardipakk.hit())  # Peidetud kaart

MängijadArv += 1  # Diiler on ka nimekirjas
i = 1
while MängijadArv > i:
    mängija = MängijaNimed[i]
    i += 1
    mängijad[mängija].uuskaart(kaardipakk.hit())
    # Kui mängija kasutas split-i, siis on vaja ainult ühte kaarti
    mängijad[mängija].uuskaart(kaardipakk.hit()) if mängijad[mängija].kaardidarv == 1 else None
    print(f"{mängija} kaardid on: {mängijad[mängija].kaardid} ning väärtus on {mängijad[mängija].väärtus}")
    ID = 1  # Antakse mängija "split" kätele (n.ö. alamkäsi)

    # Päris mängija (inimene) teeb ise valikuid
    if mängija[0:7] == "Mängija":
        while mängijad[mängija].väärtus <= 21:  # Ei ole "bust"
            valik = input("Sisesta valik: ")
            # Uus kaart
            if valik == "Hit":
                mängijad[mängija].uuskaart(kaardipakk.hit())
                print(kaardipakk.kaart)
            # Ainult üks uus kaart (topelt panus)
            elif valik == "Double" and mängijad[mängija].luba_double == 1:
                mängijad[mängija].uuskaart(kaardipakk.hit())
                print(kaardipakk.kaart)
                print(f"{mängija} kaardid on: {mängijad[mängija].kaardid} ning väärtus on {mängijad[mängija].väärtus}")
                break
            # Ei võta rohkem kaarte
            elif valik == "Stand":
                break
            # Anna alla -> kaotad väiksema panuse
            elif valik == "Surrender":
                print("Mängija andis alla")
                break
            # Split - võrdse kaardipaari puhul -> mängijal kaks kätt, mõlemal käel eraldi valikud, sama panus
            elif valik == "Split" and mängijad[mängija].luba_split == 1:
                nimi = mängija + str(ID)  # Alamkäe nimi
                ID += 1  # Juhul kui järgmine alamkäsi (uue spliti puhul)
                # Alamkäsi kui eraldi mängija
                MängijaNimed.insert(MängijaNimed.index(mängija) + 1, nimi)  # Alamkäsi mängijate nimekirja
                mängijad[nimi] = Mängija(nimi)  # Alamkäele kutsutakse välja Mängija klass
                mängijad[nimi].uuskaart(mängijad[mängija].split())  # Üks mängija kaart alammängijale
                MängijadArv += 1  # Et loop kestaks ühe mängija võrra kauem (nüüd üks mängija rohkem)
                mängijad[mängija].uuskaart(kaardipakk.hit())  # Mängijale üks kaart juurde (kuna ühe andis ära)
            # Kui ükski valik ei sobi -> vale sisestus
            else:
                print("Vale sisestus.", end=" ")
                continue

            # Kuvab mängija käe (pärast "Hit" või "Split" valikut)
            print(f"{mängija} kaardid on: {mängijad[mängija].kaardid} ning väärtus on {mängijad[mängija].väärtus}")
