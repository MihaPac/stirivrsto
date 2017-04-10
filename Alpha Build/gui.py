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
        self.igra.nova_igra()

    def zapri_okno(self, master):
        self.prekini_igralce()
        master.destroy()

    def narisi_mrezo(self):
        '''Igralno polje.'''
        self.canvas.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        sirina = 2
        for i in range(0,8):
            self.canvas.create_line(i*d, 0*d, i*d, 6*d, width = sirina, tag=Gui.TAG_OKVIR)
            self.canvas.create_line(0*d, i*d, 7*d, i*d, width = sirina, tag=Gui.TAG_OKVIR)

    def narisi_barvo(self, stolpec):
        '''Nariše krožec igralčeve barve.'''
        x = stolpec * Gui.VELIKOST_POLJA # STOLPEC
        y = self.pravo_polje(stolpec) * Gui.VELIKOST_POLJA # VRSTICA
        d1 = 5
        d2 = Gui.VELIKOST_POLJA - d1
        if self.igra.na_potezi == IGRALEC_R:
            barva = "#a55"
            igralec = "rdeči"
        elif self.igra.na_potezi == IGRALEC_M:
            barva = "#55a"
            igralec = "modri"
        else:
            print("Ni igralca!")
            return
        self.canvas.create_oval(x + d1, y + d1, x + d2, y + d2, fill=barva, tag=Gui.TAG_FIGURA)
        self.igra.povleci_potezo(stolpec, self.pravo_polje(stolpec))
        self.napis.set("Na potezi je {}.".format(igralec))

    def narisi_zmago(self, barva, trojka):
        for p in trojka:
            stolpec, vrstica = p
            x = stolpec * Gui.VELIKOST_POLJA # STOLPEC
            y = vrstica * Gui.VELIKOST_POLJA # VRSTICA
            d1 = 5
            d2 = Gui.VELIKOST_POLJA - d1
            self.canvas.create_oval(x + d1, y + d1, x + d2, y + d2, fill=barva, tag=Gui.TAG_FIGURA)
                
    def canvas_klik(self, event):
        stolpec = event.x // Gui.VELIKOST_POLJA
        vrstica = event.y // Gui.VELIKOST_POLJA
        print("Pozicija je" , stolpec, vrstica, "igralec je",
              self.igra.na_potezi)
        #zmaga = self.povleci_potezo((vrstica,stolpec))
        #print("Zmaga je {}".format(zmaga))
        self.povleci_potezo((vrstica, stolpec))
        self.konec(self.igra.stanje_igre())

    def pravo_polje(self, stolpec):
        for izbira_vrste in range(5, -1, -1):
                if self.igra.polje[stolpec][izbira_vrste] == 0:
                    return izbira_vrste
                else:
                    continue

    def povleci_potezo(self, p):
        vrstica, stolpec = p
        igralec = self.igra.na_potezi
        if self.pravo_polje(stolpec) == None:
            print("Stolpec je poln!")
            return
        self.narisi_barvo(stolpec)
        return


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
