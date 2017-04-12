from igra import *
from clovek import *
from racunalnik import *
import tkinter

globina = 1

class Gui():

    TAG_FIGURA = 'figura'

    TAG_OKVIR = 'okvir'

    VELIKOST_POLJA = 50

    def __init__(self, master, globina):
        self.igralec_m = None # Objekt, ki igra X (nastavimo ob začetku igre)
        self.igralec_r = None # Objekt, ki igra O (nastavimo ob začetku igre)
        self.igra = None # Objekt, ki predstavlja igro (nastavimo ob začetku igre)
        
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))


        menu = tkinter.Menu(master)
        master.config(menu = menu)
        #Menu za igro
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label = "Igra", menu = menu_igra)
        #Menu za izbiro igralcev
        menu_igra.add_command(label="R=Človek, M=Človek",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Clovek(self)))
        menu_igra.add_command(label="R=Človek, M=Računalnik",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Racunalnik(self, Minimax(globina))))
        menu_igra.add_command(label="R=Računalnik, M=Človek",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)),
                                                              Clovek(self)))
        menu_igra.add_command(label="R=Računalnik, M=Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)),
                                                              Racunalnik(self, Minimax(globina))))
        

        self.napis = tkinter.StringVar(master, value="Dobrodošli v 4 v vrsto!")
        tkinter.Label(master, textvariable=self.napis).grid(row=0, column=1)
        
        self.canvas = tkinter.Canvas(master, width=7*Gui.VELIKOST_POLJA, height=6*Gui.VELIKOST_POLJA)
        self.canvas.grid(row = 1, column = 1)

        self.b = tkinter.Button(master, text="Razveljavi", command = self.razveljavi)
        self.b.grid(row=2, column =0)

        self.narisi_mrezo()

        #Kontrole
        self.canvas.bind("<Button-1>", self.canvas_klik)

        #Zacetek Igre
        self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(globina)))




    def zacni_igro(self, igralec_r, igralec_m):
        self.prekini_igralce()
        # Nastavimo igralce
        self.igralec_m = Clovek(self)
        self.igralec_r = Clovek(self)
        # Pobrišemo vse figure s polja
        self.canvas.delete(Gui.TAG_FIGURA)
        self.igralec_r = igralec_r
        self.igralec_m = igralec_m
        # Ustvarimo novo igro
        self.igra = Igra()
        # Rdeči je prvi na potezi
        self.napis.set("Na potezi je rdeči.")
        self.igralec_r.igraj()

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        if self.igralec_r: self.igralec_r.prekini()
        if self.igralec_m: self.igralec_m.prekini()

    def nova_igra(self):
        self.igra.nova_igra()

    def zapri_okno(self, master):
        self.prekini_igralce()
        master.destroy()

    def narisi_mrezo(self):
        '''Igralno polje.'''
        self.canvas.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        sirina = 2
        for i in range(8):
            self.canvas.create_line(i*d + 2, 0*d + 2, i*d + 2, 6*d + 2, width = sirina, tag=Gui.TAG_OKVIR)
        for i in range(7):
            self.canvas.create_line(0*d + 2, i*d + 2, 7*d + 2, i*d + 2, width = sirina, tag=Gui.TAG_OKVIR)

    def narisi_barvo(self, stolpec, vrstica, igranje = True, igralec = None):
        '''Nariše krožec igralčeve barve.'''
        x = stolpec * Gui.VELIKOST_POLJA + 2# STOLPEC
        y = Gui.VELIKOST_POLJA * (5 - vrstica) + 2 # VRSTICA
        d1 = Gui.VELIKOST_POLJA // 10
        d2 = Gui.VELIKOST_POLJA - d1
        if igranje:
            if self.igra.na_potezi== IGRALEC_R:
                barva = "#a55"
                igralec = "modri"
            elif self.igra.na_potezi == IGRALEC_M:
                barva = "#55a"
                igralec = "rdeči"
            else:
                print("Ni igralca!")
                return
            self.canvas.create_oval(x + d1, y + d1, x + d2, y + d2, fill=barva, tag=Gui.TAG_FIGURA)
            self.igra.povleci_potezo(stolpec)
            self.napis.set("Na potezi je {}.".format(igralec))
        else:
            if igralec == IGRALEC_R:
                barva = "#a55"
                igralec = "modri"
            elif igralec == IGRALEC_M:
                barva = "#55a"
                igralec = "rdeči"
            self.canvas.create_oval(x + d1, y + d1, x + d2, y + d2, fill=barva, tag=Gui.TAG_FIGURA)


    def narisi_zmago(self, barva, trojka):
        for p in trojka:
            stolpec, vrstica = p
            x = stolpec * Gui.VELIKOST_POLJA + 2 # STOLPEC
            y = (5 - vrstica) * Gui.VELIKOST_POLJA + 2 # VRSTICA
            d1 = 5
            d2 = Gui.VELIKOST_POLJA - d1
            self.canvas.create_oval(x + d1, y + d1, x + d2, y + d2, fill=barva, tag=Gui.TAG_FIGURA)
                
    def canvas_klik(self, event):
        print(event.x, event.y)
        stolpec = event.x // Gui.VELIKOST_POLJA
        vrstica = event.y // Gui.VELIKOST_POLJA
        if event.x > Gui.VELIKOST_POLJA * 7:
            stolpec = 6
        print("Pozicija je" , stolpec, vrstica, "igralec je",
              self.igra.na_potezi)
        #zmaga = self.povleci_potezo((vrstica,stolpec))
        #print("Zmaga je {}".format(zmaga))
        self.povleci_potezo((vrstica, stolpec))
        self.konec(self.igra.stanje_igre())

    def pravo_polje(self, stolpec):
        for izbira_vrste in range(6):
                if self.igra.polje[stolpec][izbira_vrste] == 0:
                    return izbira_vrste
                else:
                    continue

    def povleci_potezo(self, p):
        vrstica, stolpec = p
        if self.pravo_polje(stolpec) == None:
            print("Stolpec je poln!")
            return
        vrstica = self.pravo_polje(stolpec)
        self.narisi_barvo(stolpec, vrstica)
        #return


    def konec(self, pogoji):
        '''Ali je konec igre?'''
        zmaga, trojka = pogoji
        if zmaga == NI_KONEC or zmaga == None:
            return
        self.igra.na_potezi = None
        zmagovalec = ""
        if zmaga == 1:
            zmagovalec = "rdeč"
            self.napis.set("Igre je konec. Zmagal je {}!".format(zmagovalec))
            self.narisi_zmago('red', trojka)
        elif zmaga == -1:
            zmagovalec = "moder"
            self.napis.set("Igre je konec. Zmagal je {}!".format(zmagovalec))
            self.narisi_zmago('blue', trojka)
        else:
            self.napis.set("Igre je konec. Nobeden ni zmagal!")

    def razveljavi(self):
        self.canvas.delete(Gui.TAG_FIGURA)
        polje = self.igra.razveljavi()
        print("Polje za razveljavo ", polje)
        for stolpec in range(6):
            for vrstica in range(5):
                if polje[stolpec][vrstica] == 1:
                    self.narisi_barvo(stolpec, vrstica, False, 1)
                elif polje[stolpec][vrstica] == -1:
                    self.narisi_barvo(stolpec, vrstica, False, -1)
        print("Narisalo se je")

if __name__ == "__main__":
    # Naredimo glavno okno in nastavimo ime
    root = tkinter.Tk()
    root.title("Štiri v vrsto")

    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplikacija = Gui(root, globina)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()        
