from igra import *
from clovek import *
import tkinter

class Gui():

    TAG_FIGURA = 'figura'

    TAG_OKVIR = 'okvir'

    VELIKOST_POLJA = 50


    def __init__(self, master):
        self.igralec_m = None # Objekt, ki igra X (nastavimo ob začetku igre)
        self.igralec_r = None # Objekt, ki igra O (nastavimo ob začetku igre)
        self.igra = None # Objekt, ki predstavlja igro (nastavimo ob začetku igre)
        
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))


        menu = tkinter.Menu(master)
        master.config(menu = menu)

        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label = "Igra", menu = menu_igra)
        menu_igra.add_command(label = "Nova igra",
                              command = self.zacni_igro)


        self.napis = tkinter.StringVar(master, value="Dobrodošli v 4 v vrsto!")
        tkinter.Label(master, textvariable=self.napis).grid(row=0, column=0)


        self.canvas = tkinter.Canvas(master, width=7*Gui.VELIKOST_POLJA, height=6*Gui.VELIKOST_POLJA)
        self.canvas.grid(row = 1, column = 0)

        self.narisi_mrezo()

        #Kontrole
        self.canvas.bind("<Button-1>", self.canvas_klik)

        #Zacetek Igre
        self.zacni_igro()

    def zacni_igro(self):
        self.prekini_igralce()
        # Nastavimo igralce
        self.igralec_m = Clovek(self)
        self.igralec_r = Clovek(self)
        # Pobrišemo vse figure s polja
        self.canvas.delete(Gui.TAG_FIGURA)
        # Ustvarimo novo igro
        self.igra = Igra()
        # Rdeči je prvi na potezi
        self.napis.set("Na potezi je rdeči.")
        self.igralec_r.igraj()
        self.nova_igra()

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        if self.igralec_r: self.igralec_r.prekini()
        if self.igralec_m: self.igralec_m.prekini()

    def nova_igra(self):
        #Naredi novo prazno matriko, ki bo predstavljala igralno polje.
        self.igra.nova_igra()

                        
        
    def koncaj_igro(self):
        self.napis.set("Igre je konec!")

    def zapri_okno(self, master):
        self.prekini_igralce()
        master.destroy()

    def narisi_mrezo(self):
        self.canvas.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        sirina = 2
        for i in range(0,8):
            self.canvas.create_line(i*d, 0*d, i*d, 6*d, width = sirina, tag=Gui.TAG_OKVIR)
            self.canvas.create_line(0*d, i*d, 7*d, i*d, width = sirina, tag=Gui.TAG_OKVIR)

    def narisi_R(self, stolpec):
        """Nariši rdec krožec v polje (i, j)."""
        x = stolpec * Gui.VELIKOST_POLJA # STOLPEC
        y = self.pravo_polje(stolpec, "R") * Gui.VELIKOST_POLJA # VRSTICA
        sirina = 1
        d1 = 5
        d2 = Gui.VELIKOST_POLJA - d1
        self.canvas.create_oval(x+d1, y+d1, x+d2, y+d2, fill="#a55",tag=Gui.TAG_FIGURA)
        self.igra.povleci_potezo(stolpec, self.pravo_polje(stolpec, "R"))
        self.napis.set("Na potezi je modri.")
        self.igra.polje[stolpec][self.pravo_polje(stolpec, "R")] = 1

    def narisi_M(self, stolpec):
        """Nariši moder krožec v polje (i, j)."""
        x = stolpec * Gui.VELIKOST_POLJA # STOLPEC
        y = self.pravo_polje(stolpec, "M") * Gui.VELIKOST_POLJA # VRSTICA
        sirina = 5
        d1 = 5
        d2 = Gui.VELIKOST_POLJA - d1
        self.canvas.create_oval(x+d1, y+d1, x+d2, y+d2, fill="#55a",tag=Gui.TAG_FIGURA)
        self.igra.povleci_potezo(stolpec, self.pravo_polje(stolpec, "R"))
        self.napis.set("Na potezi je rdeči.")
        self.igra.polje[stolpec][self.pravo_polje(stolpec, "M")] = -1
            
    def canvas_klik(self, event):
        stolpec = event.x // Gui.VELIKOST_POLJA
        vrstica = event.y // Gui.VELIKOST_POLJA
        print("Pozicija je" , stolpec, vrstica, "igralec je",
              self.igra.na_potezi)
        self.povleci_potezo((vrstica,stolpec))

    def pravo_polje(self, stolpec, barva):
        for izbira_vrste in range(5, -1, -1):
                if self.igra.polje[stolpec][izbira_vrste] == 0:
                    return izbira_vrste
                else:
                    continue

    def povleci_potezo(self, p):
        (vrstica, stolpec) = p
        igralec = self.igra.na_potezi
        print(self.igra.polje)
        if igralec == IGRALEC_R:
            #Izbere pravilno polje, da vanj narise krog
            self.narisi_R(stolpec)
        elif igralec == IGRALEC_M:
            #Izbere pravilno polje, da vanj narise krog
            self.narisi_M(stolpec)
        else:
            self.napis.set("Igre je konec.")

            
if __name__ == "__main__":
    # Naredimo glavno okno in nastavimo ime
    root = tkinter.Tk()
    root.title("Štiri v vrsto")

    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplikacija = Gui(root)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()        
