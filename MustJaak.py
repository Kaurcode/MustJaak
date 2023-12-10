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
        self.TKnimi = tk.StringVar(value=nimi)

        self.kaardid = []  # Käesolevad kaardid
        self.TKkaardid = tk.StringVar()

        self.väärtus = 0  # Kaartide väärtus kokku
        self.TKväärtus = tk.IntVar(value=0)

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

        self.TKkaardid.set(", ".join(self.kaardid))
        self.TKväärtus.set(self.väärtus)

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
    elif valik == "Us":
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
        self.aken = None
        self.langetatud_valik = None

        self.hit_nupp = None
        self.stand_nupp = None
        self.double_nupp = None
        self.surrender_nupp = None
        self.split_nupp = None

        # Mängusätete määramine
        self.MängijadArv = 7  # Mitu mängijat mängu mängib
        self.MängijaKoht = 1  # Mitmes koht on pärismängijal
        self.Kaardipakke = 4
        self.mängusätted()

        self.root.mainloop()

    def mängusätted(self):
        def edasi():
            self.MängijadArv = mängijate_arv_valik.get()
            self.MängijaKoht = mängija_koht_valik.get() - 1
            self.Kaardipakke = kaardipakid_arv_valik.get()

            self.mängu_alustamine()

        self.aken = tk.Frame(self.root)

        mängijate_arv_pealkiri = tk.Label(self.aken, text="Mängijate arv:")
        mängija_koht_pealkiri = tk.Label(self.aken, text="Mängija koht:")
        kaardipakid_arv_pealkiri = tk.Label(self.aken, text="Kaardipakke:")

        mängijate_arv_valikud = list(range(2, 8))
        mängijate_arv_valik = tk.IntVar(value=7)
        mängijad_arv_menüü = tk.OptionMenu(self.aken, mängijate_arv_valik, *mängijate_arv_valikud)

        mängija_koht_valikud = list(range(1, int(mängijate_arv_valik.get()) + 1))
        mängija_koht_valik = tk.IntVar(value=1)
        mängija_koht_menüü = tk.OptionMenu(self.aken, mängija_koht_valik, *mängija_koht_valikud)

        kaardipakid_arv_valikud = list(range(1, 9))
        kaardipakid_arv_valik = tk.IntVar(value=8)
        kaardipakid_arv_menüü = tk.OptionMenu(self.aken, kaardipakid_arv_valik, *kaardipakid_arv_valikud)

        mängijate_arv_pealkiri.pack()
        mängijad_arv_menüü.pack()

        mängija_koht_pealkiri.pack()
        mängija_koht_menüü.pack()

        kaardipakid_arv_pealkiri.pack()
        kaardipakid_arv_menüü.pack()

        valitud_nupp = tk.Button(self.aken, text="Edasi", command=edasi)
        valitud_nupp.pack()

        self.aken.pack()

    def mängu_alustamine(self):
        self.kaardipakk = Kaardipakk(self.Kaardipakke)  # Uus kaardipakk

        self.MängijaNimed = ["Arvuti" + str(i) for i in range(1, self.MängijadArv)]
        self.MängijaNimed.insert(self.MängijaKoht, "Mängija")
        self.mängijad = {nimi: Mängija(nimi) for nimi in self.MängijaNimed}

        self.diiler = Mängija("Diiler")
        self.diiler.uuskaart(self.kaardipakk.hit())  # Nähtav kaart
        print(self.kaardipakk.kaart)
        print(self.diiler.väärtus)

        self.mäng()

    def nupud(self):
        def mängijavalik(valik):
            self.nupud_olek()
            self.langetatud_valik = valik
            self.aken.quit()

        nupudosa = tk.Frame(self.aken)

        self.hit_nupp = tk.Button(nupudosa, text="Hit", state="disabled", command=lambda: mängijavalik("Hit"))
        self.hit_nupp.grid(row=0, column=0, padx=5, pady=5)

        self.stand_nupp = tk.Button(nupudosa, text="Stand", state="disabled", command=lambda: mängijavalik("Stand"))
        self.stand_nupp.grid(row=0, column=1, padx=5, pady=5)

        self.double_nupp = tk.Button(nupudosa, text="Double", state="disabled", command=lambda: mängijavalik("Double"))
        self.double_nupp.grid(row=0, column=2, padx=5, pady=5)

        self.surrender_nupp = tk.Button(nupudosa,
                                        text="Surrender", state="disabled", command=lambda: mängijavalik("Surrender"))
        self.surrender_nupp.grid(row=0, column=3, padx=5, pady=5)

        self.split_nupp = tk.Button(nupudosa, text="Split", state="disabled", command=lambda: mängijavalik("Split"))
        self.split_nupp.grid(row=0, column=4, padx=5, pady=5)

        nupudosa.pack(pady=10)

    def nupud_olek(self, olek=0):
        if olek:
            self.hit_nupp["state"] = "normal"
            self.stand_nupp["state"] = "normal"
            self.double_nupp["state"] = "normal"
            self.surrender_nupp["state"] = "normal"
            self.split_nupp["state"] = "normal"
        else:
            self.hit_nupp["state"] = "disable"
            self.stand_nupp["state"] = "disable"
            self.double_nupp["state"] = "disable"
            self.surrender_nupp["state"] = "disable"
            self.split_nupp["state"] = "disable"
        self.root.update()

    def langeta_valik(self):
        self.nupud_olek(1)
        self.aken.mainloop()
        return self.langetatud_valik

    def mängulaud(self):
        self.aken.destroy()
        self.aken = tk.Frame(self.root)

        diiler_pealkiri = tk.Label(self.aken, textvariable=self.diiler.TKnimi)
        diiler_pealkiri.pack(pady=10)

        diileri_käsi = tk.Label(self.aken, textvariable=self.diiler.TKkaardid)
        diileri_käsi.pack(pady=10)

        mängijad = tk.Frame(self.aken)

        for i in range(self.MängijadArv):
            mängija = self.mängijad[self.MängijaNimed[i]]
            self.aken.columnconfigure(i, weight=1)

            mängija_pealkiri = tk.Label(mängijad, textvariable=mängija.TKnimi)
            mängija_pealkiri.grid(row=0, column=i, padx=5, pady=5)

            mängija_käsi = tk.Label(mängijad, textvariable=mängija.TKkaardid)
            mängija_käsi.grid(row=1, column=i, padx=5, pady=5)

            väärtus_pealkiri = tk.Label(mängijad, textvariable=mängija.TKväärtus)
            väärtus_pealkiri.grid(row=2, column=i, padx=5, pady=5)

        mängijad.pack(pady=10)
        self.nupud()
        self.aken.pack()

    def mäng(self):
        self.mängulaud()
        i = 0
        while self.MängijadArv > i:
            mängija = self.mängijad[self.MängijaNimed[i]]
            i += 1
            mängija.uuskaart(self.kaardipakk.hit())
            self.root.update()
            sleep(1)
            # Kui mängija kasutas split-i, siis on vaja ainult ühte kaarti
            mängija.uuskaart(self.kaardipakk.hit()) if mängija.kaardidarv == 1 else None
            self.root.update()
            print(f"{mängija.nimi} kaardid on: {mängija.kaardid} ning väärtus on {mängija.väärtus}")
            nr = 1  # Antakse mängija "split" kätele (n.ö. alamkäsi)
            while mängija.väärtus <= 21:  # Ei ole "bust"
                # Päris mängija (inimene) teeb ise valikuid
                if mängija.nimi[0:7] == "Mängija":
                    valik = self.langeta_valik()
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
                    self.root.update()
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
                    uus_nimi = mängija.nimi + str(nr)  # Alamkäe nimi
                    nr += 1  # Juhul kui järgmine alamkäsi (uue spliti puhul)

                    # Alamkäsi kui eraldi mängija

                    # Alamkäsi mängijate nimekirja
                    self.MängijaNimed.insert(self.MängijaNimed.index(mängija.nimi) + 1, uus_nimi)
                    self.mängijad[uus_nimi] = Mängija(uus_nimi)  # Alamkäele kutsutakse välja Mängija klass
                    self.MängijadArv += 1  # Et loop kestaks ühe mängija võrra kauem (nüüd üks mängija rohkem)
                    self.mängulaud()

                    uus_mängija = self.mängijad[uus_nimi]
                    uus_mängija.uuskaart(mängija.split())  # Üks mängija kaart alammängijale
                    mängija.uuskaart(self.kaardipakk.hit())  # Mängijale üks kaart juurde (kuna ühe andis ära)
                # Kui ükski valik ei sobi -> vale sisestus
                else:
                    print("Vale sisestus.", end=" ")
                    continue

                # Kuvab mängija käe (pärast "Hit" või "Split" valikut)
                print(f"{mängija.nimi} kaardid on: {mängija.kaardid} ning väärtus on {mängija.väärtus}")
                self.root.update()
            sleep(1)
            self.root.update()


mäng = MustJaak(tk.Tk())
