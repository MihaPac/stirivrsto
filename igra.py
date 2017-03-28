import tkinter

class Gui():

    TAG_FIGURA = 'figura'

    TAG_OKVIR = 'okvir'

    VELIKOST_POLJA = 50


    def __init__(self, master):
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
        self.nova_igra()
        self.zacni_igro()

    def zacni_igro(self):
        self.canvas.delete(Gui.TAG_FIGURA)
        self.nova_igra()

    def nova_igra(self):
        #0 pomeni prazno polje
        #1 pomeni rdece polje
        #-1 pomeni modro polje
        self.matrika = [[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0]]
        self.stevec = 0
                        
        
    def koncaj_igro(self):
        self.napis.set("Igre je konec!")

    def zapri_okno(self, master):
        master.destroy()

    def narisi_mrezo(self):
        self.canvas.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        sirina = 2
        for i in range(0,8):
            self.canvas.create_line(i*d, 0*d, i*d, 6*d, width = sirina, tag=Gui.TAG_OKVIR)
            self.canvas.create_line(0*d, i*d, 7*d, i*d, width = sirina, tag=Gui.TAG_OKVIR)

    def narisi_R(self, p):
        """Nariši rdec krožec v polje (i, j)."""
        x = p[0] * Gui.VELIKOST_POLJA
        y = p[1] * Gui.VELIKOST_POLJA
        sirina = 1
        d1 = 5
        d2 = Gui.VELIKOST_POLJA - d1
        self.canvas.create_oval(x+d1, y+d1, x+d2, y+d2, fill="#a55",tag=Gui.TAG_FIGURA)

    def narisi_M(self, p):
        """Nariši moder krožec v polje (i, j)."""
        x = p[0] * Gui.VELIKOST_POLJA
        y = p[1] * Gui.VELIKOST_POLJA
        sirina = 5
        d1 = 5
        d2 = Gui.VELIKOST_POLJA - d1
        self.canvas.create_oval(x+d1, y+d1, x+d2, y+d2, fill="#55a",tag=Gui.TAG_FIGURA)
            
    def canvas_klik(self, event):
        stolpec = event.x // Gui.VELIKOST_POLJA
        vrstica = event.y // Gui.VELIKOST_POLJA
        print("Pozicija je" , stolpec, vrstica, "poteza je", self.stevec)
        self.povleci_potezo((vrstica,stolpec))

    def pravo_polje(self, stolpec, barva):
        for izbira_vrste in range(5, -1, -1):
                if self.matrika[stolpec][izbira_vrste] == 0:
                    p = (stolpec, izbira_vrste)
                    if barva == "R":
                        self.narisi_R(p)
                    elif barva == "M":
                        self.narisi_M(p)
                    self.matrika[stolpec][izbira_vrste] = -1
                    break
                else:
                    continue

    def povleci_potezo(self, p):
        (vrstica, stolpec) = p
        if self.stevec % 2 == 0:
            #Izbere pravilno polje, da vanj narise krog
            self.pravo_polje(stolpec, "R")
            self.stevec += 1
            
        else:
            #Izbere pravilno polje, da vanj narise krog
            self.pravo_polje(stolpec, "M")
            self.stevec += 1
            
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
