# -*- coding: utf8 -*-

######################################################################
## Igra

import logging

IGRALEC_M = 'M'
IGRALEC_R = 'R'
PRAZNO = '_'
NEODLOCENO = "neodločeno"
NI_KONEC = "ni konec"
VRSTICE = 6

def nasprotnik(igralec):
    """Vrni nasprotnika od igralca."""
    if igralec == IGRALEC_R:
        return IGRALEC_M
    elif igralec == IGRALEC_M:
        return IGRALEC_R
    else:
        # Do sem ne smemo priti, ÄŤe pridemo, je napaka v programu.
        # V ta namen ima Python ukaz assert, s katerim lahko preverimo,
        # ali dani pogoj velja. V naĹˇem primeru, ko vemo, da do sem
        # sploh ne bi smeli priti, napiĹˇemo za pogoj False, tako da
        # bo program crknil, ÄŤe bo priĹˇel do assert. Spodaj je Ĺˇe nekaj
        # uporab assert, kjer dejansko preverjamo pogoje, ki bi morali
        # veljati. To je zelo uporabno za odpravljanje napak.
        # Assert uporabimo takrat, ko bi program lahko deloval naprej kljub
        # napaki (ÄŤe bo itak takoj crknil, potem assert ni potreben).
        assert False, "neveljaven nasprotnik"


class Igra():
    def __init__(self):
        self.polje = [[PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO],
                      [PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO],
                      [PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO],
                      [PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO],
                      [PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO],
                      [PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO],
                      [PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO, PRAZNO]]
        self.na_potezi = IGRALEC_R
        self.zgodovina = []
        self.stevilo_potez = 0
        self.seznam = self.stirke()
        
    def shrani_pozicijo(self):
        """Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili vanjo
           z metodo razveljavi."""
        p = [self.polje[i][:] for i in range(7)]
        self.zgodovina += [(p, self.na_potezi)]

    def kopija(self):
        """Vrni kopijo te igre, brez zgodovine."""
        # Kopijo igre naredimo, ko poĹľenemo na njej algoritem.
        # ÄŚe bi algoritem poganjali kar na glavni igri, ki jo
        # uporablja GUI, potem bi GUI mislil, da se menja stanje
        # igre (kdo je na potezi, kdo je zmagal) medtem, ko bi
        # algoritem vlekel poteze
        k = Igra()
        k.polje = [self.polje[i][:] for i in range(7)]
        k.na_potezi = self.na_potezi
        return k

    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejĹˇnje stanje."""
        self.stevilo_potez -= 1
        if len(self.zgodovina) == 0:
            return "Polje je prazno"
        (self.polje, self.na_potezi) = self.zgodovina.pop()
        return self.polje

    def veljavne_poteze(self):
        """Vrni seznam veljavnih potez, v smislu kateri stolpci so prosti."""
        return [stolp for stolp in range(7) if self.polje[stolp][5] is PRAZNO]

    def prava_vrstica(self, stolpec):
        '''Vrne prvo vrstico, ki je neprazna v stolpcu. Ĺ teje od spodaj navzgor.'''
        for vrstica in range(6):
            if self.polje[stolpec][vrstica] == PRAZNO:
                return vrstica
        return None

    def povleci_potezo(self, stolp):
        """Povleci potezo p, ne naredi niÄŤ, ÄŤe je neveljavna.
           Vrne stanje_igre() po potezi ali None, ce je poteza neveljavna."""
        self.stevilo_potez += 1
        vrstica = self.prava_vrstica(stolp)
        if (vrstica == None) or (self.na_potezi == None):
            # neveljavna poteza
            logging.debug("igra: neveljavna poteza")
            return None
        else:
            self.shrani_pozicijo()
            self.polje[stolp][vrstica] = self.na_potezi
            zmagovalec, stirka = self.stanje_igre()
            if zmagovalec == NI_KONEC:
                # Igre ni konec, zdaj je na potezi nasprotnik
                self.na_potezi = nasprotnik(self.na_potezi)
            else:
                # Igre je konec
                self.na_potezi = None
            return (zmagovalec, stirka)

    def stirke(self, vrstice = 6, stolpci = 7):
        '''Prešteje vse možne Ĺˇtirke na igralni ploĹˇÄŤi in jih zapiĹˇe v
        seznam.'''
        seznam = []
        #Vodoravne
        for stolp in range(stolpci - 3):
            for vrst in range(vrstice):
                seznam.append(
                    [(stolp,vrst), (stolp + 1,vrst), (stolp + 2,vrst), (stolp + 3,vrst)])
        #Navpicne
        for stolp in range(stolpci):
            for vrst in range(vrstice - 3):
                seznam.append(
                    [(stolp,vrst), (stolp,vrst+1), (stolp,vrst+2), (stolp,vrst+3)])
        #Narascajoce diagonale
        for stolp in range(stolpci - 3):
            for vrst in range(3,vrstice):
                if stolp + vrst < 9:
                    seznam.append(
                        [(stolp,vrst), (stolp+1,vrst-1), (stolp+2,vrst-2), (stolp+3,vrst-3)])
        #Padajoce diagonale
        for stolp in range(stolpci - 3):
            for vrst in range(vrstice - 3):
                if stolp + vrst < 6:
                    seznam.append(
                        [(stolp, vrst), (stolp + 1, vrst + 1),
                         (stolp + 2, vrst + 2), (stolp + 3, vrst + 3)])
        return seznam

    def stanje_igre(self):
        """Ugotovi, kakĹˇno je trenutno stanje igre. Vrne:
           - (IGRALEC_R, stirka), ÄŤe je igre konec in je zmagal IGRALEC_R z dano zmagovalno stirko
           - (IGRALEC_M, stirka), ÄŤe je igre konec in je zmagal IGRALEC_M z dano zmagovalno stirko
           - (NEODLOCENO, None), ÄŤe je igre konec in je neodloÄŤeno
           - (NI_KONEC, None), ÄŤe igre Ĺˇe ni konec
        """
        for t in self.seznam:
            [(i1,j1),(i2,j2),(i3,j3),(i4,j4)] = t
            p = self.polje[i1][j1]
            if p != PRAZNO and p == self.polje[i2][j2] == self.polje[i3][j3] == self.polje[i4][j4]:
                # NaĹˇli smo zmagovalno trojko
                return (p, [t[0], t[1], t[2], t[3]])
        # Ni zmagovalca, ali je igre konec?
        for stolp in range(7):
            if self.polje[stolp][5] is PRAZNO:
                # NaĹˇli smo prazno plosca, igre ni konec
                return (NI_KONEC, None)
        # Vsa polja so polna, rezultat je neodloÄŤen
        return (NEODLOCENO, None)

