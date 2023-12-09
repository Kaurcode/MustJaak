import tkinter as tk
from random import shuffle, randint
from time import sleep


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


# Igal mängijal oma käsi(kaardid) ning load, mida ta teha võib
class Mängija:
    def __init__(self, nimi):
        self.nimi = nimi
        self.kaardid = []  # Käesolevad kaardid
        self.väärtus = 0  # Kaartide väärtus kokku
        self.A11 = 0  # Mitu ässa on väärtusega 11?
        self.kaardidarv = 0  # Mitu kaarti käes on? Et ei peaks kasutama len()-i

        self.luba_double = 0  # Kas mängija võib panust tõsta?
        self.luba_split = 0  # Kas mängija võib käe "kaheks" teha (split)?
        self.luba_surr = 0

        self.kaart = None  # Mis on viimati mängijale määratud kaart?
        self.kaardiväärtus = None  # Mis on viimati mängijale määratud kaardi väärtus?

    # Mängijale määratakse uus kaart
    def uuskaart(self, kaartväärtus):
        self.kaart, self.kaardiväärtus = kaartväärtus  # Kaart ise ja selle väärtus
        self.kaardid.append(self.kaart)
        self.väärtus += self.kaardiväärtus
        self.kaardidarv += 1
        self.luba_double = 1 if self.kaardidarv == 2 else 0  # Lubatakse double, kui on ainult kaks kaarti
        # Lubatakse split, kui on kaks kaarti, mis on võrdsed
        self.luba_split = 1 if self.kaardidarv == 2 and self.kaardid[0][3:] == self.kaardid[1][3:] else 0

        # Äss saab olla, kas 1 või 11, ehk kui on väärtus üle 21, siis loetakse äss üheks
        self.A11 += 1 if self.kaart[3:] == "A" else 0
        if self.väärtus > 21 and self.A11 > 0:
            self.väärtus -= 10
            self.A11 -= 1  # Ässasid, mille väärtus on 11, on nüüd ühe võrra vähem

    def split(self):
        self.väärtus -= self.kaardiväärtus  # Käe väärtus väheneb eelneva kaardi väärtuse võrra
        self.kaardidarv -= 1  # Üks kaart vähem
        return self.kaardid.pop(), self.kaardiväärtus  # Kaart antakse edasi n.ö. alamkäele(eraldi mängija)


# Olenevalt kaartidest väljastab funktsioon parima valiku
# Blackjacki basic strateegia võtsin Blackjacki Wikipeedia saidilt: https://en.wikipedia.org/wiki/Blackjack
# S = Stand; H = Hit; Dh = Double/Hit; Ds = Double/Stand; SP = Split
# Uh = Surrender/hit; Us = Surrender/stand; Usp = Surrender/split
def strateegia(mängija, diiler):
    kaardid = mängija.kaardid
    väärtus = mängija.väärtus

    paar = mängija.kaardidarv == 2  # Kas on kaks kaarti?
    pildikaart = ("J", "Q", "K")
    kaardid_pildita = ["10" if kaart[3:] in pildikaart else kaart[3:] for kaart in kaardid]  # Pildikaart = "10"

    # Diileri nähtava kaardi asukoht tabelis
    diilervõimalik = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "A")
    diilerkaart = diiler.kaardid[0][3:]
    diilerkaart = "10" if diilerkaart in pildikaart else diilerkaart
    diilerindeks = diilervõimalik.index(diilerkaart)

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
        valik = tabel[kaartindeks][diilerindeks]

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
        valik = tabel[kaartindeks][diilerindeks]

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
        valik = tabel[väärtusindeks][diilerindeks]

    if valik == "Dh":
        return "Double" if mängija.luba_double == 1 else "Hit"
    elif valik == "Ds":
        return "Double" if mängija.luba_double == 1 else "Stand"
    elif valik == "Uh":
        return "Surrender" if mängija.luba_surr == 1 else "Hit"
    elif valik == "Uh":
        return "Surrender" if mängija.luba_surr == 1 else "Stand"
    elif valik == "Usp":
        return "Surrender" if mängija.luba_surr == 1 else "Split"
    else:
        return {"H": "Hit", "S": "Stand", "SP": "Split"}[valik]


# GUI
class MustJaak:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("800x600")

        self.kaardipakk = None
        self.MängijaNimed = None
        self.mängijad = None
        self.diiler = None

        # Mängusätete määramine
        self.MängijadArv = 7  # Mitu mängijat mängu mängib
        self.MängijaKoht = 1  # Mitmes koht on pärismängijal
        self.Kaardipakke = 4
        self.mängusätted()
        self.mängu_alustamine()
        self.mäng()

    def mängusätted(self):
        def edasi():
            self.MängijadArv = MängijadArvValik.get()
            self.MängijaKoht = MängijaKohtValik.get() - 1
            self.Kaardipakke = KaardipakkeValik.get()

            self.root.destroy()

        MängijadArvPealkiri = tk.Label(self.root, text="Mängijate arv:")
        MängijaKohtPealkiri = tk.Label(self.root, text="Mängija koht:")
        KaardipakkePealkiri = tk.Label(self.root, text="Kaardipakke:")

        MängijadArvValikud = list(range(2, 8))
        MängijadArvValik = tk.IntVar(value=7)
        MängijadArvMenüü = tk.OptionMenu(self.root, MängijadArvValik, *MängijadArvValikud)

        MängijaKohtValikud = list(range(1, int(MängijadArvValik.get()) + 1))
        MängijaKohtValik = tk.IntVar(value=1)
        MängijaKohtMenüü = tk.OptionMenu(self.root, MängijaKohtValik, *MängijaKohtValikud)

        KaardipakkeValikud = list(range(1, 9))
        KaardipakkeValik = tk.IntVar(value=8)
        KaardipakkeMenüü = tk.OptionMenu(self.root, KaardipakkeValik, *KaardipakkeValikud)

        MängijadArvPealkiri.pack()
        MängijadArvMenüü.pack()

        MängijaKohtPealkiri.pack()
        MängijaKohtMenüü.pack()

        KaardipakkePealkiri.pack()
        KaardipakkeMenüü.pack()

        ValikNupp = tk.Button(self.root, text="Edasi", command=edasi)
        ValikNupp.pack()

        self.root.mainloop()

    def mängulaua_loomine(self):
        self.diileri_label = tk.Label(self.root, text="Diiler")
        self.diileri_label.pack(pady=10)

        self.diileri_käsi = tk.Label(self.root, text="")
        self.diileri_käsi.pack(pady=10)

        self.mängija_label = tk.Label(self.root, text="Mängija")
        self.mängija_label.pack(pady=10)

        self.mängija_käsi = tk.Label(self.root, text="")
        self.mängija_käsi.pack(pady=10)

        self.hit_button = tk.Button(self.root, text="Hit", command=self.hit)
        self.hit_button.pack(side="top", pady=10)

        self.stand_button = tk.Button(self.root, text="Stand", command=self.stand)
        self.stand_button.pack(side="top", pady=10)

        self.double_button = tk.Button(self.root, text="Double", command=self.double)
        self.double_button.pack(side="top", pady=10)

        self.surrender_button = tk.Button(self.root, text="Surrender", command=self.surrender)
        self.surrender_button.pack(side="top", pady=10)

        self.split_button = tk.Button(self.root, text="Split", command=self.split)
        self.split_button.pack(side="top", pady=10)

        self.mängu_alustamine()

    def mängu_alustamine(self):
        self.kaardipakk = Kaardipakk(self.Kaardipakke)  # Uus kaardipakk

        self.MängijaNimed = ["Arvuti" + str(i) for i in range(1, self.MängijadArv)]
        self.MängijaNimed.insert(self.MängijaKoht, "Mängija")
        self.mängijad = {nimi: Mängija(nimi) for nimi in self.MängijaNimed}

        self.diiler = Mängija("Diiler")
        self.diiler.uuskaart(self.kaardipakk.hit())  # Nähtav kaart
        print(self.kaardipakk.kaart)
        print(self.diiler.väärtus)
        # self.diileri_käsi["text"] = f'Diiler: {self.diiler.kaart}'
        self.diiler.uuskaart(self.kaardipakk.hit())  # Peidetud kaart

    def mäng(self):
        i = 0
        while self.MängijadArv > i:
            mängija = self.mängijad[self.MängijaNimed[i]]
            i += 1
            mängija.uuskaart(self.kaardipakk.hit())
            # Kui mängija kasutas split-i, siis on vaja ainult ühte kaarti
            mängija.uuskaart(self.kaardipakk.hit()) if mängija.kaardidarv == 1 else None
            print(f"{mängija.nimi} kaardid on: {mängija.kaardid} ning väärtus on {mängija.väärtus}")
            ID = 1  # Antakse mängija "split" kätele (n.ö. alamkäsi)

            while mängija.väärtus <= 21:  # Ei ole "bust"
                # Päris mängija (inimene) teeb ise valikuid
                if mängija.nimi[0:7] == "Mängija":
                    valik = input("Sisesta valik: ")
                else:
                    sleep(1)
                    valik = strateegia(mängija, self.diiler)
                    print(valik)
                    sleep(1)
                # Uus kaart
                if valik == "Hit":
                    mängija.uuskaart(self.kaardipakk.hit())
                    print(self.kaardipakk.kaart)
                # Ainult üks uus kaart (topelt panus)
                elif valik == "Double" and mängija.luba_double == 1:
                    mängija.uuskaart(self.kaardipakk.hit())
                    print(self.kaardipakk.kaart)
                    print(f"{mängija.nimi} kaardid on: {mängija.kaardid} ning väärtus on {mängija.väärtus}")
                    break
                # Ei võta rohkem kaarte
                elif valik == "Stand":
                    break
                # Anna alla -> kaotad väiksema panuse
                elif valik == "Surrender":
                    print(f"{mängija.nimi} andis alla")
                    break
                # Split - võrdse kaardipaari puhul -> mängijal kaks kätt, mõlemal käel eraldi valikud, sama panus
                elif valik == "Split" and mängija.luba_split == 1:
                    uus_nimi = mängija.nimi + str(ID)  # Alamkäe nimi
                    ID += 1  # Juhul kui järgmine alamkäsi (uue spliti puhul)

                    # Alamkäsi kui eraldi mängija
                    self.MängijaNimed.insert(self.MängijaNimed.index(mängija) + 1, uus_nimi)  # Alamkäsi mängijate nimekirja
                    self.mängijad[uus_nimi] = Mängija(uus_nimi)  # Alamkäele kutsutakse välja Mängija klass
                    uus_mängija = self.mängijad[uus_nimi]
                    uus_mängija.uuskaart(mängija.split())  # Üks mängija kaart alammängijale
                    self.MängijadArv += 1  # Et loop kestaks ühe mängija võrra kauem (nüüd üks mängija rohkem)
                    mängija.uuskaart(self.kaardipakk.hit())  # Mängijale üks kaart juurde (kuna ühe andis ära)
                # Kui ükski valik ei sobi -> vale sisestus
                else:
                    print("Vale sisestus.", end=" ")
                    continue

                # Kuvab mängija käe (pärast "Hit" või "Split" valikut)
                print(f"{mängija.nimi} kaardid on: {mängija.kaardid} ning väärtus on {mängija.väärtus}")

    def hit(self):
        # Logic for "Hit" button
        if self.mängija_väärtus <= 21:
            mängija_käsi, väärtus = self.kaardipakk.hit()
            self.mängija_käsi["text"] += f' {mängija_käsi}'
            self.mängija_väärtus += väärtus

            # Check if player busts
            if self.mängija_väärtus > 21:
                self.mängija_käsi["text"] += " (Bust)"
                self.end_round()

    def stand(self):
        # Logic for "Stand" button
        self.diileri_käsi["text"] = f"Diiler: {self.diileri_kaardid} (Väärtus: {self.diileri_väärtus})"
        self.resolve_round()

    def double(self):
        # Logic for "Double" button
        if self.mängija_väärtus <= 21 and self.mängija_käsi.cget("text") != "Double":
            mängija_käsi, väärtus = self.kaardipakk.hit()
            self.mängija_käsi["text"] += f' {mängija_käsi}'
            self.mängija_väärtus += väärtus
            self.stand()

    def surrender(self):
        # Logic for "Surrender" button
        if self.mängija_väärtus <= 21 and self.mängija_käsi.cget("text") != "Surrender":
            self.mängija_käsi["text"] += " (Andis alla)"
            self.end_round()

    def split(self):
        pass

    def resolve_round(self):
        # Player has stood, simulate computer's moves
        while self.diileri_väärtus < 17:  # Simulate hitting until the value is 17 or more
            diileri_käsi, väärtus = self.kaardipakk.hit()
            self.diileri_kaardid.append(diileri_käsi)
            self.diileri_käsi["text"] += f' {diileri_käsi}'
            self.diileri_väärtus += väärtus

        # Check the result and declare the winner
        if self.diileri_väärtus > 21 or (self.mängija_väärtus <= 21 and self.mängija_väärtus > self.diileri_väärtus):
            self.diileri_käsi["text"] += f" (Bust)"
            self.mängija_käsi["text"] += " (Võitja)"
        elif self.mängija_väärtus == self.diileri_väärtus:
            self.diileri_käsi["text"] += f" (Viik)"
            self.mängija_käsi["text"] += " (Viik)"
        else:
            self.mängija_käsi["text"] += " (Kaotus)"


mäng = MustJaak(tk.Tk())
