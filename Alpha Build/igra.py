######################################################################
## Igra

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
        # Do sem ne smemo priti, če pridemo, je napaka v programu.
        # V ta namen ima Python ukaz assert, s katerim lahko preverimo,
        # ali dani pogoj velja. V našem primeru, ko vemo, da do sem
        # sploh ne bi smeli priti, napišemo za pogoj False, tako da
        # bo program crknil, če bo prišel do assert. Spodaj je še nekaj
        # uporab assert, kjer dejansko preverjamo pogoje, ki bi morali
        # veljati. To je zelo uporabno za odpravljanje napak.
        # Assert uporabimo takrat, ko bi program lahko deloval naprej kljub
        # napaki (če bo itak takoj crknil, potem assert ni potreben).
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

    #def nova_igra(self):

    def shrani_pozicijo(self):
        """Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili vanjo
           z metodo razveljavi."""
        p = [self.polje[i][:] for i in range(7)]
        self.zgodovina += [(p, self.na_potezi)]
        #print("tole",self.zgodovina, "to je zgodovina")

    def kopija(self):
        """Vrni kopijo te igre, brez zgodovine."""
        # Kopijo igre naredimo, ko poženemo na njej algoritem.
        # Če bi algoritem poganjali kar na glavni igri, ki jo
        # uporablja GUI, potem bi GUI mislil, da se menja stanje
        # igre (kdo je na potezi, kdo je zmagal) medtem, ko bi
        # algoritem vlekel poteze
        k = Igra()
        k.polje = [self.polje[i][:] for i in range(7)]
        k.na_potezi = self.na_potezi
        return k

    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejšnje stanje."""
        if len(self.zgodovina) == 0:
            return "Polje je prazno"
        (self.polje, self.na_potezi) = self.zgodovina.pop()
        #print(self.polje, " je polje")
        return self.polje

    def veljavne_poteze(self):
        """Vrni seznam veljavnih potez, v smislu kateri stolpci so prosti."""
        return [stolp for stolp in range(7) if self.polje[stolp][5] is PRAZNO]

    def prava_vrstica(self, stolpec):
        for vrstica in range(6):
            if self.polje[stolpec][vrstica] == PRAZNO:
                return vrstica
        return None

    def povleci_potezo(self, stolp):
        """Povleci potezo p, ne naredi nič, če je neveljavna.
           Vrne stanje_igre() po potezi ali None, ce je poteza neveljavna."""
        vrstica = self.prava_vrstica(stolp)
        if (vrstica == None) or (self.na_potezi == None):
            # neveljavna poteza
            print("neveljavna poteza")
            return None
        else:
            self.shrani_pozicijo()
            self.polje[stolp][vrstica] = self.na_potezi
            zmagovalec, trojka = self.stanje_igre()
            if zmagovalec == NI_KONEC:
                # Igre ni konec, zdaj je na potezi nasprotnik
                self.na_potezi = nasprotnik(self.na_potezi)
                #print(self.polje)
                # print("menjal sem potezo")
            else:
                # Igre je konec
                self.na_potezi = None
            return (zmagovalec, trojka)

    # Tabela vseh trojk, ki nastopajo v igralnem polju
    trojke = []
        # Vodoravne
    for stolp in range(4):
        for vrst in range(6):
                trojke.append(
                            [(stolp,vrst), (stolp + 1,vrst), (stolp + 2,vrst), (stolp + 3,vrst)])
    #print(len(trojke))
        #Navpicne
    for stolp in range(7):
        for vrst in range(3):
                trojke.append(
                            [(stolp,vrst), (stolp,vrst+1), (stolp,vrst+2), (stolp,vrst+3)])
    #print(len(trojke))
        #Narascajoce diagonale
    for stolp in range(4):
        for vrst in range(3,6):
            if stolp + vrst < 9:
                trojke.append(
                            [(stolp,vrst), (stolp+1,vrst-1), (stolp+2,vrst-2), (stolp+3,vrst-3)])
    #print(len(trojke))
        #Padajoce diagonale
    for stolp in range(4):
        for vrst in range(3):
            if stolp + vrst < 6:
                trojke.append(
                            [(stolp, vrst), (stolp + 1, vrst + 1),
                             (stolp + 2, vrst + 2), (stolp + 3, vrst + 3)])

    #print(trojke)
    #print(len(trojke))

    def stanje_igre(self):
        """Ugotovi, kakšno je trenutno stanje igre. Vrne:
           - (IGRALEC_R, trojka), če je igre konec in je zmagal IGRALEC_R z dano zmagovalno trojko
           - (IGRALEC_M, trojka), če je igre konec in je zmagal IGRALEC_M z dano zmagovalno trojko
           - (NEODLOCENO, None), če je igre konec in je neodločeno
           - (NI_KONEC, None), če igre še ni konec
        """
        for t in self.trojke:
            [(i1,j1),(i2,j2),(i3,j3),(i4,j4)] = t
            p = self.polje[i1][j1]
            if p != PRAZNO and p == self.polje[i2][j2] == self.polje[i3][j3] == self.polje[i4][j4]:
                # Našli smo zmagovalno trojko
                return (p, [t[0], t[1], t[2], t[3]])
        # Ni zmagovalca, ali je igre konec?
        for stolp in range(7):
            if self.polje[stolp][5] is PRAZNO:
                # Našli smo prazno plosca, igre ni konec
                return (NI_KONEC, None)
        # Vsa polja so polna, rezultat je neodločen
        return (NEODLOCENO, None)
