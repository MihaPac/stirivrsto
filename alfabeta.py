# -*- coding: utf8 -*-

import logging
import random
from igra import IGRALEC_M, IGRALEC_R, PRAZNO, NEODLOCENO, NI_KONEC, nasprotnik

max_globina = 7

######################################################################
## Algoritem alfabeta

# Vrednosti igre
ZMAGA = 1000000000 # Mora biti vsaj 10^9
NESKONCNO = ZMAGA + 1 # Več kot zmaga

def pomembnost(i):
    "Vrni pomembnost poteze p. Manjše število pomeni, da je bolj pomembna."
    return (i - 3) * (i - 3)

class Alfabeta:
    # Algoritem alfabeta predstavimo z objektom, ki hrani stanje igre in
    # algoritma, nima pa dostopa do GUI (ker ga ne sme uporabljati, saj deluje
    # v drugem vlaknu kot tkinter).

    def __init__(self, globina=max_globina, alkohol = False):
        self.globina = globina  # do katere globine iščemo?
        self.prekinitev = False # ali moramo končati?
        self.igra = None # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None # sem napišemo potezo, ko jo najdemo
        self.vrednost = None # sem napišemo, kako dobra je ta poteza
        # v primeru, da izberemo pivski 4 v vrsto:
        self.alkohol = alkohol # Če je računalnik nastavljen da bo delal napake
        self.pijanost = 0 # Kako pogosto bo delal računalnik napake


    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        """Izračunaj potezo za trenutno stanje dane igre."""
        # To metodo pokličemo iz vzporednega vlakna
        assert (igra is not None)
        assert (igra.na_potezi is not None)
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        # Poženemo alfabeta
        (poteza, vrednost) = self.alfabeta(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("alfabeta: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza
            self.vrednost = vrednost



    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije: seĹˇteje vrednosti vseh trojk na ploĹˇÄŤi."""
        # Slovar, ki pove, koliko so vredne posamezne štirke, kjer "((x,y),p) : v" pomeni:
        # Če imamo v trojki x znakov igralca in y znakov nasprotnika (in 3-x-y praznih polj),
        # potem je taka štirka za self.jaz vredna v.
        # Štirke, ki se ne pojavljajo v slovarju, so vredne 0.
        vrednost_stirke = {
            #(4,0) : ZMAGA,
            #(0,4) : -ZMAGA//2,
            (3,0) : ZMAGA//1000,
            (0,3) : -ZMAGA//2000,
            (2,0) : ZMAGA//100000,
            (0,2) : -ZMAGA//200000,
            (1,0) : ZMAGA//10000000,
            (0,1) : -ZMAGA//20000000
        }
        vrednost = 0
        for t in self.igra.seznam:
            pomembnost = 100
            for polje in t:
                pomembnost = min(pomembnost, polje[1])
            x = 0
            y = 0
            for (stolp, vrst) in t:
                if self.igra.polje[stolp][vrst] == self.jaz:
                    x += 1
                elif self.igra.polje[stolp][vrst] == nasprotnik(self.jaz):
                    y += 1
                else:
                    assert (self.igra.polje[stolp][vrst] == PRAZNO)
            vrednost += vrednost_stirke.get((x,y), 0) - pomembnost * 10
        if self.alkohol == True and random.random() < 0.17:
            self.pijanost += 0.2 
        return vrednost + self.igra.stevilo_potez + self.pijanost * (10 ** (self.igra.stevilo_potez//2)) * random.choice([-1, 1])
    
    def alfabeta(self, globina, maksimiziramo, alfa = -NESKONCNO, beta = NESKONCNO):
        """Glavna metoda alfabeta."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug ("Alfabeta prekinja, globina = {0}".format(globina))
            return (None, 0)
        (zmagovalec, lst) = self.igra.stanje_igre()
        if self.igra.polje[3][0] == PRAZNO:
            return (3, 0)
        if zmagovalec in (IGRALEC_M, IGRALEC_R, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, ZMAGA - self.igra.stevilo_potez)
            elif zmagovalec == nasprotnik(self.jaz):
                return (None, -ZMAGA + self.igra.stevilo_potez)
            else:
                return (None, 0)
        elif zmagovalec == NI_KONEC:
            assert (self.igra.na_potezi == (self.jaz if maksimiziramo else nasprotnik(self.jaz)))
            if globina == max_globina:
                logging.debug("Moje poteze so: {0}".format(self.igra.veljavne_poteze()))
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo alfabeta
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost = -NESKONCNO
                    for i in sorted(self.igra.veljavne_poteze(), key=pomembnost):
                        self.igra.povleci_potezo(i)
                        v = self.alfabeta(globina-1, not maksimiziramo, alfa, beta)[1]
                        if (vrednost < v) or (vrednost == v and random.random() < 0.2):
                            najboljsa_poteza = i
                            vrednost = v
                        self.igra.razveljavi()
                        alfa = max(alfa, vrednost)
                        if beta <= alfa:
                            break

                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost = NESKONCNO
                    for i in sorted(self.igra.veljavne_poteze(), key=pomembnost):
                        self.igra.povleci_potezo(i)
                        v = self.alfabeta(globina-1, not maksimiziramo, alfa, beta)[1]
                        if (vrednost > v) or (vrednost == v and random.random() < 0.2):
                            najboljsa_poteza = i
                            vrednost = v
                        self.igra.razveljavi()
                        beta = min(beta, vrednost)
                        if beta <= alfa:
                            break

                assert (najboljsa_poteza is not None), "alfabeta: izračunana poteza je None"
                return (najboljsa_poteza, vrednost)
        else:
            assert False, "alfabeta: nedefinirano stanje igre"

