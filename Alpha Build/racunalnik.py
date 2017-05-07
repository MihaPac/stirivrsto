# -*- coding: utf8 -*-

import threading  # za vzporedno izvajanje

from alfabeta import *

######################################################################
## Igralec raÄŤunalnik

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem # Algoritem, ki izraÄŤuna potezo
        self.mislec = None # Vlakno (thread), ki razmiĹˇlja

    def igraj(self):
        """Igraj potezo, ki jo vrne algoritem."""
        # Tu sproĹľimo vzporedno vlakno, ki raÄŤuna potezo. Ker tkinter ne deluje,
        # ÄŤe vzporedno vlakno direktno uporablja tkinter (glej http://effbot.org/zone/tkinter-threads.htm),
        # zadeve organiziramo takole:
        # - poĹľenemo vlakno, ki poiĹˇÄŤe potezo
        # - to vlakno nekam zapiĹˇe potezo, ki jo je naĹˇlo
        # - glavno vlakno, ki sme uporabljati tkinter, vsakih 100ms pogleda, ali
        #   je Ĺľe bila najdena poteza (metoda preveri_potezo spodaj).
        # Ta reĹˇitev je precej amaterska. Z resno knjiĹľnico za GUI bi zadeve lahko
        # naredili bolje (vlakno bi samo sporoÄŤilo GUI-ju, da je treba narediti potezo).

        # Naredimo vlakno, ki mu podamo *kopijo* igre (da ne bo zmedel GUIja):
        self.mislec = threading.Thread(
            target=lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))

        # PoĹľenemo vlakno:
        self.mislec.start()

        # Gremo preverjat, ali je bila najdena poteza:
        self.gui.canvas.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri, ali je algoritem Ĺľe izraÄŤunal potezo."""
        #print("Preverjamo")
        if self.algoritem.poteza is not None:
            # Algoritem je naĹˇel potezo, povleci jo, ÄŤe ni bilo prekinitve
            print("RaÄŤunalnikova poteza je {0}, vredna {1}".format(self.algoritem.poteza, self.algoritem.vrednost))
            self.gui.povleci_potezo(self.algoritem.poteza)
            print("Na potezi je ",self.gui.igra.na_potezi)
            # Vzporedno vlakno ni veÄŤ aktivno, zato ga "pozabimo"
            self.mislec = None
        else:
            # Algoritem Ĺˇe ni naĹˇel poteze, preveri Ĺˇe enkrat ÄŤez 100ms
            self.gui.canvas.after(100, self.preveri_potezo)

    def prekini(self):
        # To metodo kliÄŤe GUI, ÄŤe je treba prekiniti razmiĹˇljanje.
        if self.mislec:
            logging.debug ("Prekinjamo {0}".format(self.mislec))
            # Algoritmu sporoÄŤimo, da mora nehati z razmiĹˇljanjem
            self.algoritem.prekini()
            # PoÄŤakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None

    def klik(self, p):
        # RaÄŤunalnik ignorira klike
        pass

