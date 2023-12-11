import tkinter as tk
from random import shuffle, randint
from time import sleep
from PIL import ImageTk, Image


class Kaardipakk:
    # Uus segatud kaardipakk (klassi välja kutsumisel)
    def __init__(self, pakikogus):
        # Muutuja kaardi tähistamiseks
        self.kaart = None

        # Loob kaardid ühe kaardipaki jaoks
        mastid = ("Ruutu", "Ärtu", "Poti", "Risti")
        ühikud = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
        üks_pakk = [mast + " " + ühik for mast in mastid for ühik in ühikud]

        # Määrab igale kaardile väärtuse
        väärtused = (2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11) * 4  # 4 erinevat masti, 10, J, Q, K sama väärtusega
        self.KaardiVäärtus = {kaart: väärtus for kaart, väärtus in zip(üks_pakk, väärtused)}

        # Määratud pikkusega kaardipakk, segab paki ära
        self.kaardipakk = pakikogus * üks_pakk
        shuffle(self.kaardipakk)
        self.kaardihulk = pakikogus * 52  # Kaartide kogus, et ei peaks koguaeg len()-i välja kutsuma
        self.vahekaart = randint(round(self.kaardihulk * 0.4), round(self.kaardihulk * 0.6))  # Millal uuesti segatakse?

        kaardipildid = {kaart: Image.open(f"Kaardid/{osad[0][:3] + osad[1]}.png").resize((50, 73)) for kaart, osad in
                        [(kaart, kaart.split()) for kaart in üks_pakk]}
        self.kaardipildid = {kaart: ImageTk.PhotoImage(pilt) for kaart, pilt in kaardipildid.items()}

    # Kaardipakist võetakse uus kaart
    def hit(self):
        self.kaardihulk -= 1
        self.kaart = self.kaardipakk.pop(0)
        return self.kaart, self.KaardiVäärtus[self.kaart]


# Igal mängijal oma käsi(kaardid) ning load, mida ta teha võib
class Mängija:
    def __init__(self, nimi, kaardipakk, inimene=0, ülemkäsi=None):
        self.inimene = inimene
        self.ülemkäsi = ülemkäsi

        self.nimi = nimi
        self.TKnimi = tk.StringVar(value=nimi)

        self.kaardid = []  # Käesolevad kaardid
        self.TKkaardid = tk.StringVar()
        self.kaardid_pildiga = None

        self.väärtus = 0  # Kaartide väärtus kokku
        self.TKväärtus = tk.IntVar(value=0)

        self.A11 = 0  # Mitu ässa on väärtusega 11?
        self.kaardidarv = 0  # Mitu kaarti käes on? Et ei peaks kasutama len()-i

        self.luba_double = 0  # Kas mängija võib panust tõsta?
        self.luba_split = 0  # Kas mängija võib käe "kaheks" teha (split)?
        self.luba_surr = 1

        self.kaart = None  # Mis on viimati mängijale määratud kaart?
        self.kaardiväärtus = None  # Mis on viimati mängijale määratud kaardi väärtus?
        self.tiitel = None  # Mis on viimati mängijale määratud kaardi tiitel?

        self.kaardipakk = kaardipakk
        self.x_pos = 1
        self.y_pos = 1

    # Mängijale määratakse uus kaart
    def uuskaart(self, kaartväärtus):
        self.kaart, self.kaardiväärtus = kaartväärtus  # Kaart ise ja selle väärtus

        self.kaardid.append(self.kaart)
        self.väärtus += self.kaardiväärtus
        self.tiitel = self.kaart.split()[1]

        self.kaardidarv += 1
        self.luba_double = 1 if self.kaardidarv == 2 else 0  # Lubatakse double, kui on ainult kaks kaarti
        # Lubatakse split, kui on kaks kaarti, mis on võrdsed
        self.luba_split = 1 if self.kaardidarv == 2 and self.kaardid[0].split()[1] == self.kaardid[1].split()[1] else 0

        # Äss saab olla, kas 1 või 11, ehk kui on väärtus üle 21, siis loetakse äss üheks
        self.A11 += 1 if self.tiitel == "A" else 0
        if self.väärtus > 21 and self.A11 > 0:
            self.väärtus -= 10
            self.A11 -= 1  # Ässasid, mille väärtus on 11, on nüüd ühe võrra vähem

        self.TKkaardid.set("\n".join(self.kaardid))
        self.TKväärtus.set(self.väärtus)
        self.kaardid_pildiga.create_image(self.x_pos, self.y_pos, image=self.kaardipakk.kaardipildid[self.kaart], anchor=tk.NW)
        self.x_pos += 10
        self.y_pos += 10

    def split(self):
        self.väärtus -= self.kaardiväärtus  # Käe väärtus väheneb eelneva kaardi väärtuse võrra
        self.TKväärtus.set(self.väärtus)
        self.kaardidarv -= 1  # Üks kaart vähem
        self.A11 += 1 if self.tiitel == "A" else 0
        väljuv_kaart = self.kaardid.pop()
        self.TKkaardid.set("\n".join(self.kaardid))
        return väljuv_kaart, self.kaardiväärtus  # Kaart antakse edasi n.ö. alamkäele(eraldi mängija)


# Olenevalt kaartidest väljastab funktsioon parima valiku
# Blackjacki basic strateegia võtsin Blackjacki Wikipeedia saidilt: https://en.wikipedia.org/wiki/Blackjack
# S = Stand; H = Hit; Dh = Double/Hit; Ds = Double/Stand; SP = Split
# Uh = Surrender/hit; Us = Surrender/stand; Usp = Surrender/split
def strateegia(mängija, diiler):
    kaardid = mängija.kaardid
    väärtus = mängija.väärtus

    paar = mängija.kaardidarv == 2  # Kas on kaks kaarti?
    pildikaart = ("J", "Q", "K")
    kaardid_pildita = ["10" if kaart.split()[1] in pildikaart else kaart.split()[1] for kaart in kaardid]  # Pildikaart = "10"

    # Diileri nähtava kaardi asukoht tabelis
    diilervõimalik = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "A")
    diilerkaart = diiler.kaardid[0].split()[1]
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
                 ("SP", "SP", "SP", "SP", "SP", "SP", "SP", "SP", "SP", "Usp"),  # 8,8
                 ("SP", "SP", "SP", "SP", "SP", "SP", "H", "H", "H", "H"),  # 7,7
                 ("SP", "SP", "SP", "SP", "SP", "H", "H", "H", "H", "H"),  # 6,6
                 ("Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "Dh", "H", "H"),  # 5,5
                 ("H", "H", "H", "SP", "SP", "H", "H", "H", "H", "H"),  # 4,4
                 ("SP", "SP", "SP", "SP", "SP", "SP", "H", "H", "H", "H"),  # 3,3
                 ("SP", "SP", "SP", "SP", "SP", "SP", "H", "H", "H", "H"))  # 2,2
        valik = tabel[kaartindeks][diilerindeks]

    # "Soft totals" - Pehme väärtus (kaartide seas esineb äss)
    elif mängija.A11:
        muu_väärtus = mängija.väärtus - 11
        muud_väärtused = tuple(range(10, 1, -1))
        väärtusindeks = muud_väärtused.index(muu_väärtus)
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
        valik = tabel[väärtusindeks][diilerindeks]

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
        self.root.geometry("1200x600")

        self.kaardipakk = None
        self.mängijad = None
        self.käed = None
        self.diiler = None
        self.aken = None
        self.langetatud_valik = None

        self.hit_nupp = None
        self.stand_nupp = None
        self.double_nupp = None
        self.surrender_nupp = None
        self.split_nupp = None
        self.kaardipildid = None

        # Mängusätete määramine
        self.Kaardipakke = 4
        self.MängijadArv = None
        self.KäedArv = None
        self.mängusätted()

        self.root.mainloop()

    def mängusätted(self):
        def edasi():
            self.Kaardipakke = kaardipakid_arv_valik.get()
            self.kaardipakk = Kaardipakk(self.Kaardipakke)  # Uus kaardipakk

            self.käed = [Mängija(mängija["nimi"].get(), self.kaardipakk, mängija["inimene"].get()) for mängija in p_valikud.values() if mängija["olek"].get() == 1]
            self.mängijad = {mängija.nimi: [mängija] for mängija in self.käed}

            self.MängijadArv = len(self.mängijad)
            self.KäedArv = self.MängijadArv

            self.mäng()

        self.aken = tk.Frame(self.root)

        mängijad_tabel = tk.Frame(self.aken)

        p = ["p1", "p2", "p3", "p4", "p5", "p6", "p7"]
        p_valikud = {nimi: {"olek": tk.IntVar(value=0), "inimene": tk.IntVar(value=0), "nimi": tk.StringVar()} for nimi in p}
        i = 0
        for valik in p_valikud.values():
            valik_kast = tk.Checkbutton(mängijad_tabel, text=f"Mängija {i + 1}", variable=valik["olek"], onvalue=1, offvalue=0)
            valik_kast.grid(row=0, column=i * 2, columnspan=2, padx=5, pady=5)

            arvuti_valik = tk.Checkbutton(mängijad_tabel, text="Inimene", variable=valik["inimene"], onvalue=1, offvalue=0)
            arvuti_valik.grid(row=1, column=i * 2, columnspan=2, padx=5, pady=5)

            nimi_pealkiri = tk.Label(mängijad_tabel, text="Mängija nimi: ")
            nimi_pealkiri.grid(row=2, column=i * 2, columnspan=2, padx=5, pady=5)

            nimi_väli = tk.Entry(mängijad_tabel, textvariable=valik["nimi"])
            nimi_väli.insert(tk.END, f"Mängija {i + 1}")
            nimi_väli.grid(row=3, column=i * 2, columnspan=2, padx=5, pady=5)

            i += 1

        mängijad_tabel.pack()

        kaardipakid_arv_pealkiri = tk.Label(self.aken, text="Kaardipakke:")

        kaardipakid_arv_valikud = list(range(1, 9))
        kaardipakid_arv_valik = tk.IntVar(value=8)
        kaardipakid_arv_menüü = tk.OptionMenu(self.aken, kaardipakid_arv_valik, *kaardipakid_arv_valikud)

        kaardipakid_arv_pealkiri.pack()
        kaardipakid_arv_menüü.pack()

        valitud_nupp = tk.Button(self.aken, text="Edasi", command=edasi)
        valitud_nupp.pack()

        self.aken.pack()

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
        diiler_pealkiri.pack(pady=5)

        self.diiler.kaardid_pildiga = tk.Canvas(self.aken, width=90, height=115)
        self.diiler.kaardid_pildiga.pack(pady=5)

        diileri_käsi = tk.Label(self.aken, textvariable=self.diiler.TKkaardid)
        diileri_käsi.pack(pady=5)

        väärtus_pealkiri = tk.Label(self.aken, textvariable=self.diiler.TKväärtus)
        väärtus_pealkiri.pack(pady=5)

        mängijad_aken = tk.Frame(self.aken)

        for mängija, i in zip(self.mängijad, range(self.MängijadArv)):
            self.aken.columnconfigure(i, weight=1)

            mängija_pealkiri = tk.Label(mängijad_aken, text=mängija)
            mängija_pealkiri.grid(row=0, column=i, padx=5, pady=5)

            käed = self.mängijad[mängija]
            käed_aken = tk.Frame(mängijad_aken)

            for j, käsi in enumerate(käed):
                käsi_pealkiri = tk.Label(käed_aken, text=f"Käsi #{j+1}:")
                käsi_pealkiri.grid(row=0, column=j, padx=5, pady=5)

                käsi.kaardid_pildiga = tk.Canvas(käed_aken, width=90, height=115)
                käsi.kaardid_pildiga.grid(row=1, column=j, padx=5, pady=5)

                mängija_käsi = tk.Label(käed_aken, textvariable=käsi.TKkaardid)
                mängija_käsi.grid(row=2, column=j, padx=5, pady=5)

                väärtus_pealkiri = tk.Label(käed_aken, textvariable=käsi.TKväärtus)
                väärtus_pealkiri.grid(row=3, column=j, padx=5, pady=5)

            käed_aken.grid(row=1, column=i)

        mängijad_aken.pack(pady=10)
        self.nupud()
        self.aken.pack()

    def mäng(self):
        self.diiler = Mängija("Diiler", self.kaardipakk)
        self.mängulaud()
        self.diiler.uuskaart(self.kaardipakk.hit())  # Nähtav kaart
        print(f"Diileri kaardid on: {self.diiler.kaardid} ning väärtus on {self.diiler.väärtus}")
        i = 0
        while self.KäedArv > i:
            mängija = self.käed[i]
            i += 1
            mängija.uuskaart(self.kaardipakk.hit())
            self.root.update()
            sleep(1)
            # Kui mängija kasutas split-i, siis on vaja ainult ühte kaarti
            mängija.uuskaart(self.kaardipakk.hit()) if mängija.kaardidarv == 1 else None
            self.root.update()
            print(f"{mängija.nimi} kaardid on: {mängija.kaardid} ning väärtus on {mängija.väärtus}")
            # nr = 1  # Antakse mängija "split" kätele (n.ö. alamkäsi)
            while mängija.väärtus <= 21:  # Ei ole "bust"
                # Päris mängija (inimene) teeb ise valikuid
                if mängija.inimene:
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
                    # uus_nimi = mängija.nimi + str(nr)  # Alamkäe nimi
                    # nr += 1  # Juhul kui järgmine alamkäsi (uue spliti puhul)

                    # Alamkäsi kui eraldi mängija

                    # Alamkäsi mängijate nimekirja
                    self.käed.insert(i, Mängija(mängija.nimi, mängija.inimene, mängija))  # Alamkäele kutsutakse välja Mängija klass
                    self.KäedArv += 1  # Et loop kestaks ühe mängija võrra kauem (nüüd üks mängija rohkem)

                    uus_mängija = self.käed[i]
                    self.mängijad[mängija.nimi].insert(self.mängijad[mängija.nimi].index(mängija) + 1, uus_mängija)

                    self.mängulaud()
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

        self.diiler.uuskaart(self.kaardipakk.hit())
        print(f"Diileri kaardid on: {self.diiler.kaardid} ning väärtus on {self.diiler.väärtus}")
        self.root.update()
        while self.diiler.väärtus < 17 or self.diiler.väärtus == 17 and self.diiler.A11 > 0:
            sleep(1)
            self.diiler.uuskaart(self.kaardipakk.hit())
            self.root.update()
            print(f"Diileri kaardid on: {self.diiler.kaardid} ning väärtus on {self.diiler.väärtus}")


mäng = MustJaak(tk.Tk())
