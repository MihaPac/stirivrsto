# -*- coding: utf8 -*-

######################################################################
## Igralec ÄŤlovek

class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        # Smo na potezi. Zaenkrat ne naredimo niÄŤ, ampak
        # ÄŤakamo, da bo uporanik kliknil na ploĹˇÄŤo. Ko se
        # bo to zgodilo, nas bo Gui obvestil preko metode
        # klik.
        pass

    def prekini(self):
        # To metodo kliÄŤe GUI, ÄŤe je treba prekiniti razmiĹˇljanje.
        # ÄŚlovek jo lahko ignorira.
        pass

    def klik(self, p):
        # PovleÄŤemo potezo. ÄŚe ni veljavna, se ne bo zgodilo niÄŤ.
        self.gui.povleci_potezo(p)

