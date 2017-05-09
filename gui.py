# -*- coding: utf8 -*-

from igra import *
from clovek import *
from racunalnik import *
import alfabeta
import tkinter
import argparse
import logging

class Gui():

    TAG_FIGURA = 'figura'

    TAG_OKVIR = 'okvir'

    VELIKOST_POLJA = 75
    

    def __init__(self, master, globina):
        self.igralec_m = None # Objekt, ki igra X (nastavimo ob začetku igre)
        self.igralec_r = None # Objekt, ki igra O (nastavimo ob začetku igre)
        self.igra = None # Objekt, ki predstavlja igro (nastavimo ob začetku igre)
        self.globina = 4
        self.pijanost = False # Spremenljivka, ki pove, ali računalnik dela napake

        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        menu = tkinter.Menu(master)
        master.config(menu = menu)

        #Menu za igro
        menu_igra = tkinter.Menu(menu, tearoff=0)
        menu_tezavnost = tkinter.Menu(menu, tearoff=0)
        menu_napak = tkinter.Menu(menu, tearoff=0)
        menu.add_cascade(label = "Igra", menu = menu_igra)
        menu.add_cascade(label = "Težavnost", menu = menu_tezavnost)
        
        #Težavnost, v bistvu samo nastavljanje globine
        menu_tezavnost.add_checkbutton(label="Računalnik dela napake", command=lambda: self.izberi_pijanost())
        menu_tezavnost.add("separator")
        menu_tezavnost.add_radiobutton(label="Zelo lahka igra (Globina = 3)",
                                   command=lambda: self.izberi_tezavnost(3))
        menu_tezavnost.add_radiobutton(label="Lahka igra (Globina = 4)",
                                   command=lambda: self.izberi_tezavnost(4))
        menu_tezavnost.add_radiobutton(label="Normalna igra (Globina = 5)",
                                   command=lambda: self.izberi_tezavnost(5))
        menu_tezavnost.add_radiobutton(label="Težka igra (Globina = 6)",
                                   command=lambda: self.izberi_tezavnost(6))
        
        #Menu za izbiro igralcev
        menu_igra.add_command(label="R=Človek, M=Človek",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Clovek(self)))
        menu_igra.add_command(label="R=Človek, M=Računalnik", 
                             command=lambda: self.zacni_igro(Clovek(self),
                                                              Racunalnik(self, Alfabeta(self.globina,
                                                                                        self.pijanost))))
        menu_igra.add_command(label="R=Računalnik, M=Človek",
                              command=lambda: self.zacni_igro(Racunalnik(self, Alfabeta(self.globina,
                                                                                        self.pijanost)),
                                                              Clovek(self)))
        menu_igra.add_command(label="R=Računalnik, M=Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, Alfabeta(self.globina,
                                                                                        self.pijanost)),
                                                              Racunalnik(self, Alfabeta(self.globina,
                                                                                        self.pijanost))))

        #Grafični elementi
        master.configure(background="#acd")
        self.napis = tkinter.StringVar(master, value="")
        tkinter.Label(master, font = "Impact {}".format(Gui.VELIKOST_POLJA//2),
                      width=35, textvariable=self.napis, background="#acd").grid(row=0, column=0)

        self.canvas = tkinter.Canvas(master, width=7*Gui.VELIKOST_POLJA, height=6*Gui.VELIKOST_POLJA,
                                     background="#fff")
        self.canvas.grid(row = 1, column = 0)
        
        self.b = tkinter.Button(master, text="Razveljavi", command = self.razveljavi)
        self.b.grid(row=2, column =0)
        
        self.narisi_mrezo()

        #Kontrole
        self.canvas.bind("<Button-1>", self.canvas_klik)

        #Zacetek Igre
        self.zacni_igro(Clovek(self), Racunalnik(self, Alfabeta(self.globina,
                                                                self.pijanost)))
    
    def izberi_pijanost(self):
        '''Nastavi pijanost na nasprotno vrednost, kot je bila prej.'''
        self.pijanost = not self.pijanost

    def izberi_tezavnost(self, globina):
        '''Nastavi self.globina do vrednosti globina.'''
        self.globina = globina

    def zacni_igro(self, igralec_r, igralec_m):
        '''Zbriše polje in začne novo igro z igralcema igralec_r in igralec_m,
        ki sta ali računalnika ali človeka.'''
        self.prekini_igralce()
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

    def zapri_okno(self, master):
        self.prekini_igralce()
        master.destroy()

    def narisi_mrezo(self):
        '''Nariše igralno polje s 7 stolpci in 6 vrsticami.'''
        self.canvas.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        sirina = 2
        for i in range(8):
            self.canvas.create_line(i*d + 2, 0*d + 2, i*d + 2, 6*d + 2, width = sirina, tag=Gui.TAG_OKVIR)
        for i in range(7):
            self.canvas.create_line(0*d + 2, i*d + 2, 7*d + 2, i*d + 2, width = sirina, tag=Gui.TAG_OKVIR)

    def narisi_barvo(self, stolpec, vrstica, igralec):
        '''Nariše krogec barve igralec v stolpec, vrstico igralnega polja.'''
        x = stolpec * Gui.VELIKOST_POLJA + 2# STOLPEC
        y = Gui.VELIKOST_POLJA * (5 - vrstica) + 2 # VRSTICA
        d1 = Gui.VELIKOST_POLJA // 10
        d2 = Gui.VELIKOST_POLJA - d1
        barva = ""
        if igralec == IGRALEC_M:
            barva = "#55a"
        elif igralec == IGRALEC_R:
            barva = "#a55"
        self.canvas.create_oval(x + d1, y + d1, x + d2, y + d2, fill=barva, tag=Gui.TAG_FIGURA)


    def narisi_zmago(self, barva, stirka):
        '''Ko je zaželjeno število krogcev v eni vrsti, se dodajo krogci druge barve
        nad njimi, da je zmaga bolj vidna.'''
        for p in stirka:
            stolpec, vrstica = p
            x = stolpec * Gui.VELIKOST_POLJA + 2 # STOLPEC
            y = (5 - vrstica) * Gui.VELIKOST_POLJA + 2 # VRSTICA
            d1 = 5
            d2 = Gui.VELIKOST_POLJA - d1
            self.canvas.create_oval(x + d1, y + d1, x + d2, y + d2, fill=barva, tag=Gui.TAG_FIGURA)

    def canvas_klik(self, event):
        '''Kliče clovek.py ali racunalnik.py, da povleče potezo znotraj gui.'''
        stolpec = event.x // Gui.VELIKOST_POLJA
        if event.x > Gui.VELIKOST_POLJA * 7:
            stolpec = 6
        logging.debug("gui: Pozicija klika je {0} stolpec, igralec je {1}".format(
                                stolpec, self.igra.na_potezi))
        if self.igra.na_potezi == IGRALEC_M:
            self.igralec_m.klik(stolpec)
        elif self.igra.na_potezi == IGRALEC_R:
            self.igralec_r.klik(stolpec)
        else:
            # Nihče ni na potezi, uporabnik pa klika
            pass

    def povleci_potezo(self, stolpec):
        '''Nariše krogec v pravilni poziciji z uporabo funkcije narisi_barvo.
           Znotraj igre tudi povleče potezo in spremeni zapis nad igralni
           poljem, da pove, kdo je na potezi'''
        vrstica = self.igra.prava_vrstica(stolpec)
        if vrstica == None:
            logging.debug("gui: Stolpec je poln!")
            return None
        self.narisi_barvo(stolpec, vrstica, self.igra.na_potezi)
        self.igra.povleci_potezo(stolpec)
        igralec = ""
        if self.igra.na_potezi == IGRALEC_R:
            igralec = "rdeči"
            self.napis.set("Na potezi je {}.".format(igralec))
            self.igralec_r.igraj()
        elif self.igra.na_potezi == IGRALEC_M:
            igralec = "modri"
            self.napis.set("Na potezi je {}.".format(igralec))
            self.igralec_m.igraj()
        else:
            self.konec(self.igra.stanje_igre())


    def konec(self, pogoji):
        '''Preveri, ali je konec igre.'''
        zmaga, stirka = pogoji
        if zmaga == NI_KONEC or zmaga == None:
            return
        self.igra.na_potezi = None
        zmagovalec = ""
        if zmaga == IGRALEC_R:
            zmagovalec = "rdeč"
            self.napis.set("Igre je konec. Zmagal je {}!".format(zmagovalec))
            self.narisi_zmago('red', stirka)
        elif zmaga == IGRALEC_M:
            zmagovalec = "moder"
            self.napis.set("Igre je konec. Zmagal je {}!".format(zmagovalec))
            self.narisi_zmago('blue', stirka)
        else:
            self.napis.set("Igre je konec. Nobeden ni zmagal!")

    def razveljavi(self):
        '''Razveljavi zadnjo potezo.'''
        self.canvas.delete(Gui.TAG_FIGURA)
        polje = self.igra.razveljavi()
        if type(polje) != list:
            return
        for stolpec in range(7):
            for vrstica in range(6):
                if polje[stolpec][vrstica] == IGRALEC_R:
                    self.narisi_barvo(stolpec, vrstica, IGRALEC_R)
                elif polje[stolpec][vrstica] == IGRALEC_M:
                    self.narisi_barvo(stolpec, vrstica, IGRALEC_M)
        if self.igra.na_potezi == IGRALEC_R:
            self.napis.set("Na potezi je rdeči.")
        elif self.igra.na_potezi == IGRALEC_M:
            self.napis.set("Na potezi je modri.")

if __name__ == "__main__":
    # Iz ukazne vrstice poberemo globino za minimax, uporabimo
    # modul argparse, glej https://docs.python.org/3.4/library/argparse.html

    # Opišemo argumente, ki jih sprejmemo iz ukazne vrstice
    parser = argparse.ArgumentParser(description="Igrica štiri v vrsto")
    # Argument --globina n, s privzeto vrednostjo MINIMAX_GLOBINA
    parser.add_argument('--globina',
                        default=alfabeta.max_globina,
                        type=int,
                        help='globina iskanja za minimax algoritem')
    # Argument --debug, ki vklopi sporočila o tem, kaj se dogaja
    parser.add_argument('--debug',
                        action='store_true',
                        help='vklopi sporočila o dogajanju')

    # Obdelamo argumente iz ukazne vrstice
    args = parser.parse_args()

    # Vklopimo sporočila, če je uporabnik podal --debug
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Naredimo glavno okno in nastavimo ime
    root = tkinter.Tk()
    root.title("Štiri v vrsto")

    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplikacija = Gui(root, alfabeta.max_globina)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()


