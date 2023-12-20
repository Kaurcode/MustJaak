import tkinter as tk
from tkinter import ttk
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
        self.üks_pakk = [mast + " " + ühik for mast in mastid for ühik in ühikud]

        # Määrab igale kaardile väärtuse
        väärtused = (2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11) * 4  # 4 erinevat masti, 10, J, Q, K sama väärtusega
        self.KaardiVäärtus = {kaart: väärtus for kaart, väärtus in zip(self.üks_pakk, väärtused)}

        # Määratud pikkusega kaardipakk
        self.pakikogus = pakikogus
        self.kaardipakk = None
        self.kaardihulk = None
        self.vahekaart = None
        self.sega()

        kaardipildid = {kaart: Image.open(f"Kaardid/{osad[0][:3] + osad[1]}.png").resize((50, 73)) for kaart, osad in
                        [(kaart, kaart.split()) for kaart in self.üks_pakk]}
        self.kaardipildid = {kaart: ImageTk.PhotoImage(pilt) for kaart, pilt in kaardipildid.items()}

    # Kaardipakist võetakse uus kaart
    def hit(self):
        if self.kaardihulk == 0:
            self.sega()
        self.kaardihulk -= 1
        self.kaart = self.kaardipakk.pop(0)
        # self.kaart = "Ruutu A"  # Testimiseks
        return self.kaart, self.KaardiVäärtus[self.kaart]

    def sega(self):
        # segab paki ära
        self.kaardipakk = self.pakikogus * self.üks_pakk
        shuffle(self.kaardipakk)
        self.kaardihulk = self.pakikogus * 52  # Kaartide kogus, et ei peaks koguaeg len()-i välja kutsuma
        self.vahekaart = randint(round(self.kaardihulk * 0.4), round(self.kaardihulk * 0.6))  # Millal uuesti segatakse?


# Igal mängijal oma käsi(kaardid) ning load, mida ta teha võib
class Mängija:
    def __init__(self, nimi, kaardipakk, inimene=0, žetoonid=None, ülemkäsi=None, split=0):
        self.inimene = inimene
        self.ülemkäsi = ülemkäsi

        self.nimi = nimi
        self.TKnimi = tk.StringVar(value=nimi)
        self.žetoonid = žetoonid
        self.panus = None

        self.kaardid = []  # Käesolevad kaardid
        self.TKkaardid = tk.StringVar()
        self.kaardid_pildiga = None

        self.split_arv = split  # Mitu korda on tehtud splitti?
        self.blackjack = 0  # Kas kaardid teevad kokku blackjack-i?
        self.väärtus = 0  # Kaartide väärtus kokku
        self.TKväärtus = tk.IntVar(value=0)

        self.TKvalik = tk.StringVar()

        self.A11 = 0  # Mitu ässa on väärtusega 11?
        self.kaardidarv = 0  # Mitu kaarti käes on? Et ei peaks kasutama len()-i

        self.luba_double = 0  # Kas mängija võib panust tõsta?
        self.luba_split = 0  # Kas mängija võib käe "kaheks" teha (split)?
        self.luba_surr = 1  # Kas mängija võib "alla anda"

        self.kaart = None  # Mis on viimati mängijale määratud kaart?
        self.kaardiväärtus = None  # Mis on viimati mängijale määratud kaardi väärtus?
        self.tiitel = None  # Mis on viimati mängijale määratud kaardi tiitel?
        self.pime_kaart = None
        self.pimekaardi_väärtus = None

        self.kaardipakk = kaardipakk
        self.x_pos = 1
        self.y_pos = 1

        self.aktiivsuskast = None
        self.aktiivsustaust = None
        self.pealkiri = None
        self.kaardiväli = None
        self.väärtus_pealkiri = None
        self.valiku_kast = None

    def uus_mäng(self):
        self.kaardid = []  # Käesolevad kaardid
        self.TKkaardid.set("")
        self.kaardid_pildiga = None

        self.split_arv = 0  # Mitu korda on tehtud splitti?
        self.blackjack = 0  # Kas kaardid teevad kokku blackjack-i?
        self.väärtus = 0  # Kaartide väärtus kokku
        self.TKväärtus.set(0)

        self.TKvalik.set("")

        self.A11 = 0  # Mitu ässa on väärtusega 11?
        self.kaardidarv = 0  # Mitu kaarti käes on? Et ei peaks kasutama len()-i

        self.luba_double = 0  # Kas mängija võib panust tõsta?
        self.luba_split = 0  # Kas mängija võib käe "kaheks" teha (split)?
        self.luba_surr = 1  # Kas mängija võib "alla anda"

        self.kaart = None  # Mis on viimati mängijale määratud kaart?
        self.kaardiväärtus = None  # Mis on viimati mängijale määratud kaardi väärtus?
        self.tiitel = None  # Mis on viimati mängijale määratud kaardi tiitel?
        self.pime_kaart = None
        self.pimekaardi_väärtus = None

        self.x_pos = 1
        self.y_pos = 1

    # Mängijale määratakse uus kaart
    def uuskaart(self, kaartväärtus):
        self.kaart, self.kaardiväärtus = kaartväärtus  # Kaart ise ja selle väärtus
        self.kaardid.append(self.kaart)
        self.väärtus += self.kaardiväärtus
        self.tiitel = self.kaart.split()[1]

        self.kaardidarv += 1
        if self.kaardidarv == 2:
            self.luba_double = 1  # Lubatakse double, kui on ainult kaks kaarti
            self.luba_surr = 1
            # Lubatakse split, kui on kaks kaarti, mis on võrdsed
            self.luba_split = 1 if self.väärtus / 2 == self.kaardiväärtus else 0
            if self.split_arv == 0 and self.väärtus == 21:
                self.blackjack = 1
                self.TKvalik.set("Blackjack")
        elif self.kaardidarv == 3:
            self.luba_double = 0
            self.luba_surr = 0
            self.luba_split = 0

        # Äss saab olla, kas 1 või 11, ehk kui on väärtus üle 21, siis loetakse äss üheks
        self.A11 += 1 if self.tiitel == "A" else 0
        if self.väärtus > 21 and self.A11 > 0:
            self.väärtus -= 10
            self.A11 -= 1  # Ässasid, mille väärtus on 11, on nüüd ühe võrra vähem
            if self.väärtus > 21 and self.A11 > 0:
                self.väärtus -= 10
                self.A11 -= 1  # Ässasid, mille väärtus on 11, on nüüd ühe võrra vähem

        self.TKkaardid.set("\n".join(self.kaardid))
        self.TKväärtus.set(self.väärtus)
        self.kaardid_pildiga.config(width=50 + self.x_pos, height=73 + self.y_pos)
        self.kaardid_pildiga.create_image(self.x_pos, self.y_pos, image=self.kaardipakk.kaardipildid[self.kaart],
                                          anchor=tk.NW)
        self.x_pos += 10
        self.y_pos += 10

    def uus_pime_kaart(self, kaartväärtus):
        self.pime_kaart, self.pimekaardi_väärtus = kaartväärtus

    def näita_pime_kaart(self):
        self.uuskaart((self.pime_kaart, self.pimekaardi_väärtus))

    def split(self):
        self.väärtus -= self.kaardiväärtus  # Käe väärtus väheneb eelneva kaardi väärtuse võrra
        self.väärtus += 10 if self.tiitel == "A" else 0
        self.A11 += 1 if self.tiitel == "A" else 0
        self.TKväärtus.set(self.väärtus)
        self.kaardidarv -= 1  # Üks kaart vähem
        väljuv_kaart = self.kaardid.pop()
        self.TKkaardid.set("\n".join(self.kaardid))
        self.uuenda_pildikaarte()
        return väljuv_kaart, self.kaardiväärtus  # Kaart antakse edasi n.ö. alamkäele(eraldi mängija)

    def uuenda_pildikaarte(self):
        self.kaardid_pildiga.delete("all")
        self.x_pos = 1
        self.y_pos = 1
        for i in range(self.kaardidarv):
            self.kaardid_pildiga.config(width=50 + self.x_pos, height=73 + self.y_pos)
            self.kaardid_pildiga.create_image(self.x_pos, self.y_pos,
                                              image=self.kaardipakk.kaardipildid[self.kaardid[i]], anchor=tk.NW)
            self.x_pos += 10
            self.y_pos += 10

    def aktiivne(self, aktiivsus=0):
        if aktiivsus:
            self.aktiivsuskast.configure(bg="green")
            self.aktiivsustaust.configure(bg="lightgreen")
            self.kaardid_pildiga.config(bg="lightgreen")
            self.pealkiri.configure(background="lightgreen")
            # self.kaardiväli.configure(background="lightgreen")
            self.valiku_kast.configure(background="lightgreen")
            self.väärtus_pealkiri.configure(background="lightgreen")
        else:
            self.aktiivsuskast.configure(bg="blue")
            self.aktiivsustaust.configure(bg="lightblue")
            self.kaardid_pildiga.config(bg="lightblue")
            self.pealkiri.configure(background="lightblue")
            # self.kaardiväli.configure(background="lightblue")
            self.valiku_kast.configure(background="lightblue")
            self.väärtus_pealkiri.configure(background="lightblue")


# Olenevalt kaartidest väljastab funktsioon parima valiku
# Blackjacki basic strateegia võtsin Blackjacki Wikipeedia saidilt: https://en.wikipedia.org/wiki/Blackjack
# S = Stand; H = Hit; Dh = Double/Hit; Ds = Double/Stand; SP = Split
# Uh = Surrender/hit; Us = Surrender/stand; Usp = Surrender/split
def strateegia(mängija, diiler):
    kaardid = mängija.kaardid
    väärtus = mängija.väärtus

    paar = mängija.kaardidarv == 2  # Kas on kaks kaarti?
    pildikaart = ("J", "Q", "K")
    # Pildikaart = "10"
    kaardid_pildita = ["10" if kaart.split()[1] in pildikaart else kaart.split()[1] for kaart in kaardid]

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
    elif mängija.A11 and mängija.kaardidarv > 1:
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
        self.stiil = ttk.Style()
        self.stiil.theme_use("vista")
        taustapildifail = "Lisad/taust.jpg"
        self.taustapilt = Image.open(taustapildifail)
        self.taustapilt_tk = ImageTk.PhotoImage(self.taustapilt)

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
        self.žetoonid = (1, 5, 25, 100, 500)
        self.MängijadArv = None
        self.KäedArv = None
        self.mängusätted()

        self.root.mainloop()

    def mängusätted(self):
        def edasi():
            self.Kaardipakke = int(kaardipakid_arv_valik.get())
            self.kaardipakk = Kaardipakk(self.Kaardipakke)  # Uus kaardipakk

            self.käed = [Mängija(mängija["nimi"].get(), self.kaardipakk, mängija["inimene"].get(), mängija["žetoonid"])
                         for mängija in p_valikud.values() if mängija["olek"].get() == 1]
            for mängija in self.käed:
                mängija.panus = {väärtus: tk.StringVar(value="0") for väärtus in self.žetoonid}
                mängija.panus["kokku"] = tk.StringVar(value="0")
            self.mängijad = {mängija.nimi: [mängija] for mängija in self.käed}

            self.MängijadArv = len(self.mängijad)
            self.KäedArv = self.MängijadArv

            self.mäng()

        def liida_žetoone(väärtus, mängija):
            algne = int(mängija["žetoonid"][väärtus].get())
            mängija["žetoonid"][väärtus].set(str(algne + 1))
            algne_kokku = int(mängija["žetoonid"]["kokku"].get())
            mängija["žetoonid"]["kokku"].set(str(algne_kokku + väärtus))

        def lahuta_žetoone(väärtus, mängija):
            algne = int(mängija["žetoonid"][väärtus].get())
            mängija["žetoonid"][väärtus].set(str(algne - 1))
            algne_kokku = int(mängija["žetoonid"]["kokku"].get())
            mängija["žetoonid"]["kokku"].set(str(algne_kokku - väärtus))

        self.aken = ttk.Frame(self.root)

        mängijad_tabel = ttk.Frame(self.aken)

        p = ["p1", "p2", "p3", "p4", "p5", "p6", "p7"]
        p_valikud = {nimi: {"olek": tk.IntVar(value=0), "inimene": tk.IntVar(value=0), "nimi": tk.StringVar(),
                            "žetoonid": {"kokku": tk.StringVar(value="1875"), 1: tk.StringVar(value="25"),
                                         5: tk.StringVar(value="20"), 25: tk.StringVar(value="10"),
                                         100: tk.StringVar(value="5"), 500: tk.StringVar(value="2")}}
                     for nimi in p}
        i = 0
        for valik in p_valikud.values():
            valik_kast = ttk.Checkbutton(mängijad_tabel,
                                         text=f"Mängija {i + 1}", variable=valik["olek"], onvalue=1, offvalue=0)
            valik_kast.grid(row=0, column=i * 2, columnspan=2, padx=5, pady=5)

            arvuti_valik = ttk.Checkbutton(mängijad_tabel,
                                           text="Inimene", variable=valik["inimene"], onvalue=1, offvalue=0)
            arvuti_valik.grid(row=1, column=i * 2, columnspan=2, padx=5, pady=5)

            nimi_pealkiri = ttk.Label(mängijad_tabel, text="Mängija nimi: ")
            nimi_pealkiri.grid(row=2, column=i * 2, columnspan=2, padx=5, pady=5)

            nimi_väli = ttk.Entry(mängijad_tabel, textvariable=valik["nimi"])
            nimi_väli.insert(tk.END, f"Mängija {i + 1}")
            nimi_väli.grid(row=3, column=i * 2, columnspan=2, padx=5, pady=5)

            žetoonid_pealkiri = ttk.Label(mängijad_tabel, text="Žetoonid:")
            žetoonid_pealkiri.grid(row=4, column=i * 2, columnspan=2, padx=5, pady=5)

            žetoonid_valik = ttk.Frame(mängijad_tabel)
            žetoonid_näit = ttk.Entry(žetoonid_valik, justify="center", textvariable=valik["žetoonid"]["kokku"])
            žetoonid_näit.configure(state="readonly")
            žetoonid_näit.grid(row=0, column=0, columnspan=3, pady=5)

            for j, žetoon in enumerate(self.žetoonid):
                j += 1
                žetoon_pealkiri = ttk.Label(žetoonid_valik, text=str(žetoon))
                žetoon_nupp_m = ttk.Button(žetoonid_valik, text="-", width=3,
                                           command=lambda väärtus=žetoon, mängija=valik:
                                           lahuta_žetoone(väärtus, mängija))
                žetoon_näit = ttk.Entry(žetoonid_valik, width=10, justify="center",
                                        textvariable=valik["žetoonid"][žetoon])
                žetoon_näit.configure(state="readonly")
                žetoon_nupp_p = ttk.Button(žetoonid_valik, text="+", width=3,
                                           command=lambda väärtus=žetoon, mängija=valik:
                                           liida_žetoone(väärtus, mängija))

                žetoon_pealkiri.grid(row=2 * j - 1, column=0, columnspan=3)
                žetoon_nupp_m.grid(row=2 * j, column=0, pady=5)
                žetoon_näit.grid(row=2 * j, column=1, pady=5)
                žetoon_nupp_p.grid(row=2 * j, column=2, pady=5)

            žetoonid_valik.grid(row=5, column=i * 2, columnspan=2, padx=5, pady=5)

            i += 1

        mängijad_tabel.pack(pady=5)

        kaardipakid_arv_pealkiri = ttk.Label(self.aken, text="Kaardipakke:")

        kaardipakid_arv_valikud = [str(i) for i in range(1, 9)]
        kaardipakid_arv_valik = tk.StringVar(value="6")
        kaardipakid_arv_menüü = ttk.Combobox(self.aken, textvariable=kaardipakid_arv_valik,
                                             values=kaardipakid_arv_valikud, state="readonly")

        kaardipakid_arv_pealkiri.pack()
        kaardipakid_arv_menüü.pack(pady=5)

        valitud_nupp = ttk.Button(self.aken, text="Edasi", command=edasi)
        valitud_nupp.pack(pady=5)

        self.aken.pack()

    def nupud(self):
        def mängijavalik(valik):
            self.nupud_olek()
            self.langetatud_valik = valik
            self.aken.quit()

        nupudosa = ttk.Frame(self.aken)

        self.hit_nupp = ttk.Button(nupudosa, text="Hit", state="disabled", command=lambda: mängijavalik("Hit"))
        self.hit_nupp.grid(row=0, column=0, padx=5, pady=5)

        self.stand_nupp = ttk.Button(nupudosa, text="Stand", state="disabled", command=lambda: mängijavalik("Stand"))
        self.stand_nupp.grid(row=0, column=1, padx=5, pady=5)

        self.double_nupp = ttk.Button(nupudosa, text="Double", state="disabled", command=lambda: mängijavalik("Double"))
        self.double_nupp.grid(row=0, column=2, padx=5, pady=5)

        self.surrender_nupp = ttk.Button(nupudosa,
                                         text="Surrender", state="disabled", command=lambda: mängijavalik("Surrender"))
        self.surrender_nupp.grid(row=0, column=3, padx=5, pady=5)

        self.split_nupp = ttk.Button(nupudosa, text="Split", state="disabled", command=lambda: mängijavalik("Split"))
        self.split_nupp.grid(row=0, column=4, padx=5, pady=5)

        nupudosa.grid(row=6, column=0, pady=5)

    def nupud_olek(self, olek=0, mängija=None):
        if olek:
            self.hit_nupp["state"] = "normal"
            self.stand_nupp["state"] = "normal"
            self.double_nupp["state"] = "normal" if mängija.luba_double else "disable"
            self.surrender_nupp["state"] = "normal" if mängija.luba_surr else "disable"
            self.split_nupp["state"] = "normal" if mängija.luba_split else "disable"
        else:
            self.hit_nupp["state"] = "disable"
            self.stand_nupp["state"] = "disable"
            self.double_nupp["state"] = "disable"
            self.surrender_nupp["state"] = "disable"
            self.split_nupp["state"] = "disable"
        self.root.update()

    def langeta_valik(self, mängija):
        self.nupud_olek(1, mängija)
        self.aken.mainloop()
        return self.langetatud_valik

    def mängulaud(self):
        self.aken.destroy()
        self.aken = ttk.Frame(self.root)

        self.aken.rowconfigure(5, weight=1)

        taust = tk.Canvas(self.aken, width=0, height=0)

        self.diiler.aktiivsustaust = tk.Canvas(self.aken, width=110, height=1, highlightthickness=0)
        self.diiler.aktiivsustaust.grid(row=0, rowspan=5, column=0, sticky="ns", pady=10)

        self.diiler.pealkiri = ttk.Label(self.aken, textvariable=self.diiler.TKnimi)
        self.diiler.pealkiri.grid(row=0, column=0, pady=15)

        self.diiler.kaardid_pildiga = tk.Canvas(self.aken, width=50, height=73, highlightthickness=0)
        self.diiler.kaardid_pildiga.grid(row=1, column=0)
        self.diiler.uuenda_pildikaarte()

        # self.diiler.kaardiväli = ttk.Label(self.aken, textvariable=self.diiler.TKkaardid)
        # self.diiler.kaardiväli.grid(row=2, column=0, pady=5)

        self.diiler.väärtus_pealkiri = ttk.Label(self.aken, textvariable=self.diiler.TKväärtus)
        self.diiler.väärtus_pealkiri.grid(row=2, column=0)

        self.diiler.valiku_kast = tk.Label(self.aken, textvariable=self.diiler.TKvalik)
        self.diiler.valiku_kast.grid(row=3, column=0, padx=5, pady=5, sticky="ns")

        self.diiler.aktiivsuskast = tk.Canvas(self.aken, width=100, height=5)
        self.diiler.aktiivsuskast.grid(row=4, column=0, pady=15)
        self.diiler.aktiivne()

        mängijad_aken = ttk.Frame(self.aken)

        for mängija, i in zip(self.mängijad, range(self.MängijadArv)):
            self.aken.columnconfigure(i, weight=1)

            mängija_pealkiri = ttk.Label(mängijad_aken, text=mängija)
            mängija_pealkiri.grid(row=0, column=i, padx=5, pady=5)

            käed = self.mängijad[mängija]
            käed_aken = ttk.Frame(mängijad_aken)

            for j, käsi in enumerate(käed):

                käsi.aktiivsustaust = tk.Canvas(käed_aken, width=1, height=1)
                käsi.aktiivsustaust.grid(row=0, rowspan=5, column=j, sticky="nsew")

                käsi.pealkiri = ttk.Label(käed_aken, text=f"Käsi #{j+1}:")
                käsi.pealkiri.grid(row=0, column=j, padx=5, pady=5, sticky="ns")

                käsi.kaardid_pildiga = tk.Canvas(käed_aken, width=51, height=74, highlightthickness=0)
                käsi.kaardid_pildiga.grid(row=1, column=j, padx=5, pady=5, sticky="ns")
                käsi.uuenda_pildikaarte()

                # käsi.kaardiväli = ttk.Label(käed_aken, textvariable=käsi.TKkaardid)
                # käsi.kaardiväli.grid(row=2, column=j, padx=5, pady=5, sticky="ns")

                käsi.väärtus_pealkiri = ttk.Label(käed_aken, textvariable=käsi.TKväärtus)
                käsi.väärtus_pealkiri.grid(row=2, column=j, padx=5, pady=5, sticky="ns")

                käsi.valiku_kast = tk.Label(käed_aken, textvariable=käsi.TKvalik)
                käsi.valiku_kast.grid(row=3, column=j, padx=5, pady=5, sticky="ns")

                käsi.aktiivsuskast = tk.Canvas(käed_aken, width=100, height=5)
                käsi.aktiivsuskast.grid(row=4, column=j, padx=5, pady=5, sticky="sew")
                käsi.aktiivne()

            käed_aken.grid(row=1, column=i, sticky="sew")

        mängijad_aken.grid(row=5, column=0)

        self.nupud()
        self.aken.pack()
        self.root.update()

        self.taustapilt = self.taustapilt.resize((self.root.winfo_width(), self.root.winfo_height()))
        self.taustapilt_tk = ImageTk.PhotoImage(self.taustapilt)
        taust.create_image(0, 0, anchor=tk.NW, image=self.taustapilt_tk)
        taust.grid(column=0, row=0, rowspan=7, sticky="nsew")
        taust.config(width=self.taustapilt.width, height=self.taustapilt.height)

    def lopp_aken(self):
        kusimus_aken = tk.Toplevel(self.root)
        kusimus_aken.title("Uus mäng?")
        kusimus_aken.geometry("300x200+500+250")

        kusimus_pealkiri = ttk.Label(kusimus_aken, text="Raund läbi, uuesti?")
        kusimus_pealkiri.pack(pady=20)

        nupudosa = ttk.Frame(kusimus_aken)

        def nupp(valik):
            kusimus_aken.destroy()
            self.aken.quit()
            self.käed = [käsi for käsi in self.käed if not käsi.ülemkäsi]
            self.mängijad = {mängija.nimi: [mängija] for mängija in self.käed}
            self.MängijadArv = len(self.mängijad)
            self.KäedArv = self.MängijadArv
            for mängija in self.käed:
                mängija.uus_mäng()

            if valik == "Raund":
                self.mäng()
            elif valik == "Mäng":
                self.aken.destroy()
                self.mängusätted()
            else:
                self.root.destroy()

        uus_raund_nupp = ttk.Button(nupudosa, text="Uus raund", command=lambda: nupp("Raund"))
        uus_raund_nupp.grid(row=0, column=0, padx=5, pady=5)

        uus_mang_nupp = ttk.Button(nupudosa, text="Uus mäng", command=lambda: nupp("Mäng"))
        uus_mang_nupp.grid(row=0, column=1, padx=5, pady=5)

        valju_nupp = ttk.Button(nupudosa, text="Välju", command=lambda: nupp("Välju"))
        valju_nupp.grid(row=0, column=2, padx=5, pady=5)

        nupudosa.pack(pady=30)

        self.aken.mainloop()

    def raha_žetooniks(self, mängija, raha):
        väärtused = {"kokku": 0}
        kordaja = 1 / (len(self.žetoonid) // 2 + 1)
        for i, žetoon in enumerate(self.žetoonid[::-1]):
            hulk = raha // žetoon // max((2 - i * kordaja), 1)
            hulk = min(hulk, int(mängija.žetoonid[žetoon].get()))
            väärtused[žetoon] = int(hulk)
            väärtus = žetoon * hulk
            väärtused["kokku"] += int(väärtus)
            raha -= väärtus
        for žetoon, hulk in väärtused.items():
            mängija.panus[žetoon].set(str(hulk))

    def panustamine(self):
        rahad = {mängija: {žetoon: tk.StringVar(value=väärtus.get()) for žetoon, väärtus in mängija.žetoonid.items()}
                 for mängija in self.käed}

        def liida_žetoone(väärtus, mängitav):
            algne_panus = int(mängitav.panus[väärtus].get())
            mängitav.panus[väärtus].set(str(algne_panus + 1))
            algne = int(rahad[mängitav][väärtus].get())
            rahad[mängitav][väärtus].set(str(algne - 1))

            algne_panus_kokku = int(mängitav.panus["kokku"].get())
            mängitav.panus["kokku"].set(str(algne_panus_kokku + väärtus))
            algne_kokku = int(rahad[mängitav]["kokku"].get())
            rahad[mängitav]["kokku"].set(str(algne_kokku - väärtus))

        def lahuta_žetoone(väärtus, mängitav):
            algne_panus = int(mängitav.panus[väärtus].get())
            mängitav.panus[väärtus].set(str(algne_panus - 1))
            algne = int(rahad[mängitav][väärtus].get())
            rahad[mängitav][väärtus].set(str(algne + 1))

            algne_panus_kokku = int(mängitav.panus["kokku"].get())
            mängitav.panus["kokku"].set(str(algne_panus_kokku - väärtus))
            algne_kokku = int(rahad[mängitav]["kokku"].get())
            rahad[mängitav]["kokku"].set(str(algne_kokku + väärtus))

        self.aken.destroy()
        self.aken = ttk.Frame(self.root)
        for i, mängija in enumerate(self.käed):
            if not int(mängija.panus["kokku"].get()) or False in [int(väärtus.get()) <=
                                                                  int(mängija.žetoonid[žetoon].get())
                                                                  for žetoon, väärtus in mängija.panus.items()]:
                self.raha_žetooniks(mängija, int(mängija.žetoonid["kokku"].get()) * 0.05)
            for žetoon in rahad[mängija]:
                rahad[mängija][žetoon].set(str(int(rahad[mängija][žetoon].get()) - int(mängija.panus[žetoon].get())))
            nimi = ttk.Label(self.aken, text=mängija.nimi)
            nimi.grid(column=i, row=0, pady=5)
            rahanäit_h = ttk.Label(self.aken, text="Raha:")
            rahanäit_h.grid(column=i, row=1, pady=3)
            rahanäit = ttk.Entry(self.aken, justify="center", textvariable=rahad[mängija]["kokku"])
            rahanäit.configure(state="readonly")
            rahanäit.grid(column=i, row=2)
            panus_näit_h = ttk.Label(self.aken, text="Panus:")
            panus_näit_h.grid(column=i, row=3, pady=3)
            panus_näit = ttk.Entry(self.aken, justify="center", textvariable=mängija.panus["kokku"])
            panus_näit.configure(state="readonly")
            panus_näit.grid(column=i, row=4)
            žetoonid_valik = ttk.Frame(self.aken)

            for j, žetoon in enumerate(self.žetoonid):
                žetoon_pealkiri = ttk.Label(žetoonid_valik, text=str(žetoon))
                žetoon_nupp_m = ttk.Button(žetoonid_valik, text="-", width=3,
                                           command=lambda väärtus=žetoon, mängitav=mängija:
                                           lahuta_žetoone(väärtus, mängitav))
                alles_näit = ttk.Entry(žetoonid_valik, width=10, justify="center",
                                       textvariable=rahad[mängija][žetoon])
                alles_näit.configure(state="readonly")
                žetoon_näit = ttk.Entry(žetoonid_valik, width=10, justify="center", textvariable=mängija.panus[žetoon])
                žetoon_näit.configure(state="readonly")
                žetoon_nupp_p = ttk.Button(žetoonid_valik, text="+", width=3,
                                           command=lambda väärtus=žetoon, mängitav=mängija:
                                           liida_žetoone(väärtus, mängitav))

                žetoon_pealkiri.grid(row=3 * j, column=0, columnspan=3, pady=2)
                alles_näit.grid(row=3 * j + 1, column=0, columnspan=3)
                žetoon_nupp_m.grid(row=3 * j + 2, column=0, pady=1)
                žetoon_näit.grid(row=3 * j + 2, column=1, pady=1)
                žetoon_nupp_p.grid(row=3 * j + 2, column=2, pady=1)

            žetoonid_valik.grid(row=5, column=i, padx=5, pady=5)

        edasi_nupp = ttk.Button(self.aken, text="Edasi", command=lambda: self.aken.quit())
        edasi_nupp.grid(row=6, columnspan=self.MängijadArv)
        self.aken.pack()
        self.aken.mainloop()

    def tagastusraha(self, mängija, kordaja):
        mängija = mängija.ülemkäsi if mängija.ülemkäsi else mängija
        summa = 0
        uus_summa = int(int(mängija.panus["kokku"].get()) * kordaja)
        mängija.žetoonid["kokku"].set(str(int(mängija.žetoonid["kokku"].get()) + uus_summa))

        for žetoon in self.žetoonid:
            hulk = int(mängija.panus[žetoon].get())
            uus_hulk = int(hulk * kordaja)
            summa += uus_hulk * žetoon
            žetoonid = int(mängija.žetoonid[žetoon].get())
            mängija.žetoonid[žetoon].set(str(žetoonid + uus_hulk))
        vahe = uus_summa - summa
        print(vahe)
        if vahe > 0:
            for žetoon in self.žetoonid[::-1]:
                hulk = vahe // žetoon
                vahe -= hulk * žetoon
                mängija.žetoonid[žetoon].set(str(int(mängija.žetoonid[žetoon].get()) + hulk))

    def mäng(self):
        self.panustamine()
        for mängija in self.käed:
            for žetoon in mängija.panus:
                mängija.žetoonid[žetoon].set(str(int(mängija.žetoonid[žetoon].get()) -
                                                 int(mängija.panus[žetoon].get())))
        self.diiler = Mängija("Diiler", self.kaardipakk)
        self.mängulaud()
        if self.kaardipakk.vahekaart < self.kaardipakk.kaardihulk:
            self.kaardipakk.sega()
        i = 0
        while self.KäedArv * 2 > i:
            mängija = self.käed[i % self.KäedArv]
            mängija.uuskaart(self.kaardipakk.hit())
            print(f"{mängija.nimi} kaardid on: {mängija.kaardid} ning väärtus on {mängija.väärtus}")
            self.root.update()
            sleep(0.5)
            i += 1
            if self.KäedArv == i:
                self.diiler.uuskaart(self.kaardipakk.hit())  # Nähtav kaart
                self.root.update()
                sleep(0.5)

        self.diiler.uus_pime_kaart(self.kaardipakk.hit())  # Peidetud kaart
        self.root.update()
        print(f"Diileri kaardid on: {self.diiler.kaardid} ning väärtus on {self.diiler.väärtus}")

        if self.diiler.väärtus + self.diiler.pimekaardi_väärtus == 21:
            self.diiler.aktiivne(1)
            self.diiler.näita_pime_kaart()
            self.diiler.valiku_kast.config(fg="red")
            self.root.update()
            sleep(0.5)
            self.diiler.aktiivne()
        else:
            i = 0

        while self.KäedArv > i:
            mängija = self.käed[i]
            mängija.aktiivne(1)
            self.root.update()
            print(f"{mängija.nimi} kaardid on: {mängija.kaardid} ning väärtus on {mängija.väärtus}")
            i += 1
            sleep(0.5)
            # nr = 1  # Antakse mängija "split" kätele (n.ö. alamkäsi)
            while mängija.väärtus < 21:  # Ei ole "bust" või "blackjack"
                # Päris mängija (inimene) teeb ise valikuid
                if mängija.inimene:
                    valik = self.langeta_valik(mängija)
                else:
                    sleep(0.5)
                    valik = strateegia(mängija, self.diiler)
                    print(valik)
                mängija.TKvalik.set(valik)
                # Uus kaart
                if valik == "Hit":
                    mängija.uuskaart(self.kaardipakk.hit())
                # Ainult üks uus kaart (topelt panus)
                elif valik == "Double" and mängija.luba_double == 1:
                    mängija.uuskaart(self.kaardipakk.hit())
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
                    # Alamkäsi kui eraldi mängija
                    # Alamkäsi mängijate nimekirja
                    # Alamkäele kutsutakse välja Mängija klass
                    ülemkäsi = mängija.ülemkäsi if mängija.ülemkäsi else mängija
                    self.käed.insert(i, Mängija(mängija.nimi, self.kaardipakk, mängija.inimene, ülemkäsi=ülemkäsi,
                                                split=mängija.split_arv))
                    self.KäedArv += 1  # Et loop kestaks ühe mängija võrra kauem (nüüd üks mängija rohkem)

                    uus_mängija = self.käed[i]
                    self.mängijad[mängija.nimi].insert(self.mängijad[mängija.nimi].index(mängija) + 1, uus_mängija)
                    for käsi in self.mängijad[mängija.nimi]:
                        käsi.split_arv += 1

                    self.mängulaud()
                    uus_mängija.uuskaart(mängija.split())  # Üks mängija kaart alammängijale
                    self.root.update()
                    sleep(0.5)
                    mängija.uuskaart(self.kaardipakk.hit())  # Mängijale üks kaart juurde (kuna ühe andis ära)
                    self.root.update()
                    sleep(0.5)
                    uus_mängija.uuskaart(self.kaardipakk.hit())
                    mängija.aktiivne(1)
                # Kui ükski valik ei sobi -> vale sisestus
                else:
                    print("Vale sisestus.", end=" ")
                    continue
                # Kuvab mängija käe (pärast "Hit" või "Split" valikut)
                print(f"{mängija.nimi} kaardid on: {mängija.kaardid} ning väärtus on {mängija.väärtus}")
                self.root.update()
            mängija.aktiivne()
            self.root.update()

        if self.diiler.kaardidarv == 1:
            self.diiler.aktiivne(1)
            self.diiler.näita_pime_kaart()
            print(f"Diileri kaardid on: {self.diiler.kaardid} ning väärtus on {self.diiler.väärtus}")
            self.root.update()
            sleep(0.5)
            while self.diiler.väärtus < 17 or self.diiler.väärtus == 17 and self.diiler.A11 > 0:
                self.diiler.TKvalik.set("Hit")
                self.diiler.uuskaart(self.kaardipakk.hit())
                self.root.update()
                print(f"Diileri kaardid on: {self.diiler.kaardid} ning väärtus on {self.diiler.väärtus}")
                sleep(0.5)
            if self.diiler.väärtus > 21:
                self.diiler.TKvalik.set("Bust")
            else:
                self.diiler.TKvalik.set("Stand")
            self.diiler.aktiivne()
            self.root.update()
            sleep(0.5)
        for mängija in self.käed:
            if mängija.TKvalik.get() == "Surrender":
                mängija.valiku_kast.config(fg="red")
                self.tagastusraha(mängija, 0.5)
            elif self.diiler.blackjack:
                if mängija.blackjack:
                    mängija.TKvalik.set("Push")
                    mängija.valiku_kast.config(fg="yellow")
                    self.tagastusraha(mängija, 1)
                else:
                    mängija.TKvalik.set("Loss")
                    mängija.valiku_kast.config(fg="red")
            elif mängija.blackjack:
                mängija.valiku_kast.config(fg="green")
                self.tagastusraha(mängija, 2.5)
            elif mängija.väärtus > 21:
                mängija.TKvalik.set("Bust")
                mängija.valiku_kast.config(fg="red")
            elif mängija.väärtus == self.diiler.väärtus:
                mängija.TKvalik.set("Push")
                mängija.valiku_kast.config(fg="yellow")
                self.tagastusraha(mängija, 1)
            elif self.diiler.väärtus > 21:
                mängija.TKvalik.set("Win")
                mängija.valiku_kast.config(fg="green")
                self.tagastusraha(mängija, 2)
            elif mängija.väärtus > self.diiler.väärtus:
                mängija.TKvalik.set("Win")
                mängija.valiku_kast.config(fg="green")
                self.tagastusraha(mängija, 2)
            else:
                mängija.TKvalik.set("Loss")
                mängija.valiku_kast.config(fg="red")
            self.root.update()
            sleep(0.5)

        self.lopp_aken()


mäng = MustJaak(tk.Tk())
