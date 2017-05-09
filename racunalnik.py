# -*- coding: utf8 -*-

import threading  # za vzporedno izvajanje
import logging

from alfabeta import *

######################################################################
## Igralec računalnik

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem # Algoritem, ki izračuna potezo
        self.mislec = None # Vlakno (thread), ki razmišlja

    def igraj(self):
        """Igraj potezo, ki jo vrne algoritem."""
        # Tu sprožimo vzporedno vlakno, ki računa potezo. Ker tkinter ne deluje,
        # če vzporedno vlakno direktno uporablja tkinter (glej http://effbot.org/zone/tkinter-threads.htm),
        # zadeve organiziramo takole:
        # - poženemo vlakno, ki poišče potezo
        # - to vlakno nekam zapiše potezo, ki jo je našlo
        # - glavno vlakno, ki sme uporabljati tkinter, vsakih 100ms pogleda, ali
        #   je že bila najdena poteza (metoda preveri_potezo spodaj).

        # Naredimo vlakno, ki mu podamo *kopijo* igre (da ne bo zmedel GUIja):
        self.mislec = threading.Thread(
            target=lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))

        # Poženemo vlakno:
        self.mislec.start()

        # Gremo preverjat, ali je bila najdena poteza:
        self.gui.canvas.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri, ali je algoritem že izračunal potezo."""
        if self.algoritem.poteza is not None:
            # Algoritem je našel potezo, povleci jo, če ni bilo prekinitve
            logging.debug("racunalnik: Računalnikova poteza je {0}, vredna {1}".format(self.algoritem.poteza, self.algoritem.vrednost))
            self.gui.povleci_potezo(self.algoritem.poteza)
            # Vzporedno vlakno ni več aktivno, zato ga "pozabimo"
            self.mislec = None
        else:
            # Algoritem še ni našel poteze, preveri še enkrat čez 100ms
            self.gui.canvas.after(100, self.preveri_potezo)

    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        if self.mislec:
            logging.debug ("Prekinjamo {0}".format(self.mislec))
            # Algoritmu sporočimo, da mora nehati z razmišljanjem
            self.algoritem.prekini()
            # Počakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None

    def klik(self, p):
        # Računalnik ignorira klike
        pass

