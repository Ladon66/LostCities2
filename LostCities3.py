#
# Lost Cities
#

import random
import pygame


class Konstanten:
    AMBER = 0
    WEISS = 1
    BLAU = 2
    GRUEN = 3
    ROT = 4
    SPIELER1 = 1
    SPIELER2 = 2
    farbeL = [AMBER, WEISS, BLAU, GRUEN, ROT]      # Alle Farben
    werteL = [0, 0, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Null steht für die Wette
    farbkuerzel = ['a','w','b','g','r']
    abstandKartenX = 70           # Position der Karten die der Spieler 1 auf der Hand hält
    abstandKartenY = 30           # So liegen die Karten in den Farbstapeln untereinander
    POS_TALON = (650,800)         # Position auf der der Talon liegt
    POS_BRETT = (10,300)        # Position auf der das Brett liegt
k = Konstanten

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()      # Wofür braucht man das?
# Framerate auf 30 Frames pro Sekunde beschränken.
clock.tick(30)


# Definitionen für die Buttons
ACTIVE_COLOR = pygame.Color('dodgerblue1')
INACTIVE_COLOR = pygame.Color('dodgerblue4')
FONT = pygame.font.Font(None, 20)

cnumber = 0                 # Ist nur der Zähler

#Bilder laden
spielbrett = pygame.image.load("pic/lc_brett.png")
talon = pygame.image.load("pic/lc_rueck.png")


# Button-Technik ist geklaut von hier:
# https://stackoverflow.com/questions/47639826/pygame-button-single-click
def draw_button(button, screen):
    """Draw the button rect and the text surface."""
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


def create_button(x, y, w, h, text, callback):
    """A button is a dictionary that contains the relevant data.
    Consists of a rect, text surface and text rect, color and a callback function. """
    # The button is a dictionary consisting of the rect, text,
    # text rect, color and the callback function.
    text_surf = FONT.render(text, True, pygame.Color('white'))
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': INACTIVE_COLOR,
        'callback': callback,
        }
    return button


def increment_number():  # A callback function for the button.
        """Increment the `number` in the enclosing scope."""
        global cnumber
        cnumber += 1
        print(cnumber)


def quit_spiel():  # A callback function for the button.
  print("quit Spiel")
  pygame.quit()

def tunix(): # tut nix - button 4 braucht eine callback-Routine im Hintergrund.
    #print("tu nix")
    pass

def print_Spielsituation():
    gesamt = 0
    print("-----------------------------------")
    print("Drucke die Spielsituation")
    print_Karten("Talon: ", s.talon)                              # wieviel Karten sind noch im Talon
    gesamt = gesamt + len(s.talon)
    print_Karten("Handkarten des Spielers: ", s1.handkarten)       # Meine Handkarten
    gesamt = gesamt + len(s1.handkarten)
    # Meine bereits ausgelegten Karten
    for z in k.farbeL:
          zz = "Ablagestapel des Spielers: " + k.farbkuerzel[z] + " "
          print_Karten(zz, s1.ablagestapel[z])   
          gesamt = gesamt + len(s1.ablagestapel[z])
          print("Wert:", s.berechneWert(s1.ablagestapel[z]))
    # Vom Gegner bereits ausgelegten Karten
    for z in k.farbeL:
          zz = "Ablagestapel des Gegners: " + k.farbkuerzel[z] + " "
          print_Karten(zz, s2.ablagestapel[z]) 
          gesamt = gesamt + len(s2.ablagestapel[z])
          print("Wert:", s.berechneWert(s2.ablagestapel[z]))
    print_Karten("Abwurfstapel: ", s.abwurfstapel)              # Die bisher weggeworfenen Karten
    gesamt = gesamt + len(s.abwurfstapel)
    print_Karten("Handkarten des Gegners: ", s2.handkarten)
    gesamt = gesamt + len(s2.handkarten)
    print("Gesamtanzahl Karten:", gesamt)
    print("-----------------------------------")




button1 = create_button(10,  10, 150, 50, 'Zähle hoch', increment_number)
#button2 = create_button(170, 10, 150, 50, 'Starte Spiel', starte_spiel)
button2 = create_button(170,  10, 150, 50, 'Spielsituation', print_Spielsituation)
button3 = create_button(330,  10, 150, 50, 'Beende Spiel', quit_spiel)
button4 = create_button(800, 950, 120, 50, 'Nachzieh: 44', tunix)  # Größe des Talons
button5 = create_button(800, 890, 120, 50, 'Ablage: 00', tunix)  # Größe des Abwurfstapels
# A list that contains all buttons.
button_list = [button1, button2, button3, button4, button5]
screen.fill(pygame.Color('white'))
for button in button_list:
    draw_button(button, screen)
pygame.display.update()

class Spiel:
    # s1 ist der menschliche Spieler, s2 der Computerspieler.
    # s ist das Spiel als Ganzes
    # sie werden weiter unten definiert.
    global s1, s2, s
    anfangsstapel = []
    def __init__(self):
        print("init Spiel")
        for f in k.farbeL:
            for w in k.werteL:
                karte = Karte(f,w)
                self.anfangsstapel.append(karte) 
        random.shuffle(self.anfangsstapel)
        #print("gib Karten an die beiden Spieler")
        s1.handkarten = self.anfangsstapel[:8]
        s2.handkarten = self.anfangsstapel[8:16]
        self.talon = self.anfangsstapel[16:]
        self.abwurfstapel = []
        # vorsichtshalber machen wir auch den Anfangsstapel leer
        self.anfangsstapel = []
        # Jetzt sortieren wir die Stapel
        s1.handkarten.sort(key=lambda x: x.index)
        s2.handkarten.sort(key=lambda x: x.index)
        # Hier müssen wir jetzt den Spieler übergeben, auch wenn das hier nix
        # bringt
        self.displayKarten("Brett",[])
        self.displayKarten("HandkartenS1",s1.handkarten)
        self.displayKarten("Talon",[])

    # Hier werden die Karten gemischt und ausgegeben,
    # Und es wird auch die Ausgangsposition dargestellt.
    def starteSpiel():
        print("starte Spiel")
        for f in k.farbeL:
            for w in k.werteL:
                karte = Karte(f,w)
                s.anfangsstapel.append(karte) 
        random.shuffle(s.anfangsstapel)
        print("gib Karten an die beiden Spieler")
        s.handkarten1 = s.anfangsstapel[:8]
        s.handkarten2 = s.anfangsstapel[8:16]
        s.nachziehstapel = s.anfangsstapel[16:]
        s.anfangsstapel = [] # vorsichtshalber machen wir den Misch-Stapel leer
        # Jetzt sortieren wir die Stapel
        s.handkarten1.sort(key=lambda x: x.index)
        s.handkarten2.sort(key=lambda x: x.index)
        #print_Karten("handkarten1: ", s.handkarten1)
        #print_Karten("handkarten2: ", s.handkarten2)
        #print_Karten("Nachziehstapel: ", s.nachziehstapel)
        #print_Karten("Misch-Stapel: ", s.anfangsstapel)

    def berechneWert(self, stapeL):
      if len(stapeL) == 0:
         return (0)
      # Den Wett-Faktor ermitteln
      wett = 1
      for k in stapeL:
        if k.wert == 0:
          wett = wett + 1
      # Den Wert aller Karten ermitteln
      wert = 0
      for k in stapeL:
        wert = wert + k.wert
      # ab acht ausgespielten Karten gibt es einen Bonus
      if len(stapeL) > 7:
        bonus = 20
      else:
        bonus = 0
      # endgültige Formel: (20 sind die Expeditionskosten)
      #print ("wett: ", wett, "wert: ", wert, "bonus: ", bonus)
      return ((wert - 20) * wett + bonus)

    #Die Karten werden je nach stapel an ihrem bestimmten Ort angezeigt
    def displayKarten(self, stapelname, kL):
        #print ("display Karten", stapelname)
        if stapelname == "HandkartenS1":
            # HandkartenS1 vorher löschen
            pygame.draw.rect(screen,pygame.Color('white'),(s1.posKartenx,s1.posKarteny,630,200))
            # Koordinaten für den Start des Auslegens
            x = s1.posKartenx
            y = s1.posKarteny
            for karte in kL:
              screen.blit(karte.image,(x,y))
              x = x + k.abstandKartenX
        elif stapelname == "Brett":
            # x bestimmt die horizontale Position, y bestimmt die vertikale
            # Postition!!
            screen.blit(spielbrett, k.POS_BRETT)
        elif stapelname == "Talon":
            screen.blit(talon,k.POS_TALON)
        elif stapelname in k.farbkuerzel:
            x = s1.posFx[k.farbkuerzel.index(stapelname)]
            y = s1.posFy
            #print("da stehen wir: ",x,y)
            for karte in kL:
               screen.blit(karte.image,(x,y))
               y = y + k.abstandKartenY
        elif stapelname[1] == "2" and stapelname[0] in k.farbkuerzel:
            x = s2.posFx[k.farbkuerzel.index(stapelname[0])]
            y = s2.posFy
            #print("da stehen wir: ",x,y)
            for karte in kL:
               screen.blit(karte.image,(x,y))
               y = y + k.abstandKartenY
        else:
            print("Der Stapel ", stapelname, " kann noch nicht angezeigt werden")
        pygame.display.update()

    def display_talon(self,zz):
        #print ("Display Talon")
        zz = "Nachzieh: " + str(zz)       
        text_surf = FONT.render((zz), True, pygame.Color('white'))
        button4['text'] = text_surf
        draw_button(button4, screen) 
        pygame.display.update()

    def display_abwurfstapel(self,zz):
        #print ("Display Abwurfstapel")
        zz = "Ablage: " + str(zz)        
        text_surf = FONT.render((zz), True, pygame.Color('white'))
        button5['text'] = text_surf
        draw_button(button5, screen)
        pygame.display.update()

    def animiere_Talonkarte(self, karte):
        #print ("Animiere Talonkarte:", k.farbkuerzel[karte.farbe], karte.wert)
        pass
    
    def spielEnde(self):
        print("-----------------------------------")
        print("Spiel ist zu Ende")
    # Vom Gegner bereits ausgelegten Karten
        zz2 = 0
        print("Punkte Gegner: ", end='')
        for z in k.farbeL:
          print(str(s.berechneWert(s2.ablagestapel[z])),"/", end='')
          zz2 = zz2 + s.berechneWert(s2.ablagestapel[z])
        print("Punkte Gesamt: ", zz2)
        zz1 = 0
        print("Punkte Spieler: ", end='')
        for z in k.farbeL:
          print(str(s.berechneWert(s1.ablagestapel[z])),"/", end='')
          zz1 = zz1 + s.berechneWert(s1.ablagestapel[z])
        print("Punkte Gesamt: ", zz1)
        print("-----------------------------------")
        if zz1 > zz2:
           print("Spieler hat gewonnen")
        elif zz1 == zz2:
           print("Unentschieden")
        else:
           print("Computer hat gewonnen")
        print("-----------------------------------")






class Spieler:
    def __init__(self, sNr):
        #print ("init Spieler", sNr)
        self.handkarten = []
        self.ablagestapel = {k.AMBER:[],k.WEISS:[],k.BLAU:[],k.GRUEN:[], k.ROT:[]}
        # Die ganzen Positionen der abgegelgten Stapel kommen auch hierher.
        # Spieler Nr.  1 ist immer der Mensch:
        if sNr == 1:
            self.spieler = k.SPIELER1
            self.posFx = {k.AMBER:70,k.WEISS:240,k.BLAU:410,k.GRUEN:580, k.ROT:750}
            self.posFy = 380
            self.posKartenx = 10       # X-Position der Karten die der Spieler 1 auf der Hand hält
            self.posKarteny = 800      # Y-Position der Karten die der Spieler 1 auf der Hand hält
        elif sNr == 2:
            self.spieler = k.SPIELER2
            self.posFx = {k.AMBER:70,k.WEISS:240,k.BLAU:410,k.GRUEN:580, k.ROT:750}
            self.posFy = 100

    # Funktion für das Auslegen einer Karte
    # hier unterscheiden wir zwischen Mensch und Maschine
    def legeKarteAus(self, karte):
        #print("Lege Karte aus: ",f,w, "Spieler:", self.spieler, "Pos
        #Farbkarten y:", self.posFy)
        # Die Liste des Spielers 1 in der entsprechenden Farbe holen
        # Cooler Trick mit Dictionaries:
        actL = self.ablagestapel[karte.farbe]
        #print_Karten("legeAus",actL)
        # Wenn man die Karte anlegen kann
        if len(actL) == 0 or actL[-1].wert <= karte.wert:
            actL.append(karte)
            self.handkarten.remove(karte)
        else:  # wenn nicht, das darf eigentlich nicht passieren
            print("kann Karte nicht hinlegen", k.farbkuerzel[karte.farbe], str(karte.wert))
            return(False)
        # Die Liste ins Dictionary zurückschreiben
        self.ablagestapel[karte.farbe] = actL
        # Bei der Gelegenheit gleich mal den Stapelwert berechnen:
        #zz = s.berechneWert(actL)
        #print ("Stapelwert: ", zz)
        # Jetzt ziehen wir aber auch gleich vom Talon
        if len(s.talon) > 0:
           zzk = s.talon.pop()
           self.handkarten.append(zzk)
           # Dann noch die Karten ordnen
           self.handkarten.sort(key=lambda x: x.index)
           s.animiere_Talonkarte(zzk)


        # Grafik anpassen
        if self.spieler == k.SPIELER1:
            s.displayKarten("HandkartenS1",self.handkarten)
            s.displayKarten(k.farbkuerzel[karte.farbe], self.ablagestapel[karte.farbe])
        else:
            # Handkarten gibt es hier nicht zum Auslegen.
            zzf = k.farbkuerzel[karte.farbe] + "2"
            s.displayKarten(zzf, self.ablagestapel[karte.farbe])
        # Jetzt noch schreiben wie viele Karten im Talon sind:
        s.display_talon(str(len(s.talon)))
        return True

    def legeAufAbwurfstapel(self, karte):
        #print ("Lege auf Abwurfstapel")
        s.abwurfstapel.append(karte)
        self.handkarten.remove(karte)
        s.display_abwurfstapel(str(len(s.abwurfstapel)))
        if len(s.talon) > 0:
           zzk = s.talon.pop()
           self.handkarten.append(zzk)
           # Dann noch die Karten ordnen
           self.handkarten.sort(key=lambda x: x.index)
           s.animiere_Talonkarte(zzk)
        else:
            print("Talon ist null")
        if self.spieler == k.SPIELER1:
            s.displayKarten("HandkartenS1",self.handkarten)
        s.display_talon(str(len(s.talon)))
        return True

    #
    # Das macht nur ein Computerspieler
    # Hier kommt die ganze Logik hin!!!
    # Hier wird es spannend!!!
    #

    def waehleKarte(self):
        # Für's Erste ganz einfach: Nimm die erste Karte
        l = Loesung(str(len(s.talon)),       # wieviel Karten sind noch im Talon
                   self.handkarten,         # Handkarten des Computergegners
                   self.ablagestapel,       # Die ausgelegten Karten des Computergegners
                   s1.ablagestapel,         # Die bereits ausgelegten Karten des Spielers
                   s.abwurfstapel)         # Die bisher weggeworfenen Karten
        (aktion, pos) = l.findeZug()         # Wir geben keine Karte zurück sondern die Position im Handstapel
                                           # Bei der Aktion gibt es
                                                                               # "ausspielen" und "ablegen"
        return (aktion, pos)

class Loesung:
    # Dann hab ich alles an Informationen um den perfekten Zug zu finden:
    def __init__(self, lT,
                 hk,
                 ase,
                 asg,
                 aw):
        self.lenTalon = lT
        self.handkarten = hk
        self.ablagestapel_eigen = ase
        self.ablagestapel_gegner = asg
        self.abwurfstapel = aw

        #
        # Die allereinfachste Zug-Routine:
        # nimm eine zufällige Karte aus dem Handstapel,
        # und lege sie ab
        #

    def findeZug(self):
        karte = random.choice(self.handkarten)
        actL = self.ablagestapel_eigen[karte.farbe]
        if len(actL) == 0 or actL[-1].wert < karte.wert:
            return ("ausspielen",karte)
        else:
            return ("ablegen", karte)


    def findeZug2(self):
        print_Karten("Handkarten Gegner: ", self.handkarten)
        # In diesem Dictionary bewerten wir die Handkarten:
        self.zugwertHK = []
        # Quickwin1: Vorsichtshalber keine w-Karten ausspielen, sondern
        #            immer abwerfen
        # Quickwin2: Wenn man eine Karte, die eins höher ist, direkt anlegen
        #            kann, dann machen wir das
        # Quickwin3: Mit der Anzahl der Karten ab Ablagestapel arbeiten!!!!!!!
        #
        for k in self.handkarten:
           actL = self.ablagestapel_eigen[k.farbe]
           if len(actL) > 0 and (actL[-1].wert) + 1 == k.wert:
               print("Quickwin!")
               return ("ausspielen",k)
        # Wenn man die Karte nicht anlegen kann, setze Zugwert -1
        for nr in range(0,8):
           actL = self.ablagestapel_eigen[self.handkarten[nr].farbe]
           if len(actL) > 0 and actL[-1].wert > self.handkarten[nr].wert:
               self.zugwertHK.append(-1)
           else:
               self.zugwertHK.append(0)
        print("Zugwert: ", self.zugwertHK)
        # Wenn zu viele nicht ablegbare Karten auf der Hand sind:
        # Die erste davon ablegen!!!
        if self.zugwertHK.count(-1) > random.choice([2,3,4]):
            print("Lege Karte ab!")
            return ("ablegen",self.handkarten[self.zugwertHK.index(-1)])
        # Wenn man mehrere Karten einer Farbe auf der Hand hat,
        # Dann markiere die ungünstigen mit -1
        zwHK = self.zugwertHK
        for nr in range(0,7):
             if self.handkarten[nr].farbe == self.handkarten[nr + 1].farbe:
               if self.zugwertHK[nr] == 0 and self.zugwertHK[nr + 1] == 0:
                   print("xx", end="")
                   zwHK[nr + 1] = -1 
               else:
                   print("yy", end="")

        self.zugwertHK = zwHK
        print("Zugwert: ", self.zugwertHK)

        # gebe die Karte mit der höchsten Wertung aus zugwertHK zurück:
        highestPos = 0
        highestVal = self.zugwertHK[0]
        for nr in range(1,7):
            if self.zugwertHK[nr] >= highestVal:
                highestPos = nr
                highestVal = self.zugwertHK[nr]
                #print ("Pos:", str(highestPos), "Val", str(highestVal) )
        print("Ausspielen der Karte Nr.", str(highestPos))
        return ("ausspielen", self.handkarten[highestPos])



class Karte:
  def __init__(self,f,w):
      self.farbe = f
      self.wert = w
      self.index = self.farbe * 11 + self.wert
      if self.wert == 0:
        z = '00'
      elif self.wert == 10:
        z = '10'
      else:
        z = '0' + str(self.wert)
      zz = "pic/lc_" + k.farbkuerzel[self.farbe] + "_" + z + ".png"
      self.image = pygame.image.load(zz)
      #print ("Image :", zz)
      #print ("nach init: ",farbkuerzel[self.farbe], self.wert, self.index)


# Ausdruck der übergebenen Kartenliste
def print_Karten(stapelname, kL):
  print(stapelname)
  for karte in kL:
    print(k.farbkuerzel[karte.farbe],karte.wert,end="/")
  print("Karten gesamt: ", len(kL))

s1 = Spieler(1) # Menschlicher Spieler
s2 = Spieler(2) # Computerspieler
s = Spiel()



#
#   Hier kommt das eigentliche Hauptprogramm
#
#   Als nächstes:
#   Maus und Hauptschleife so umbauen wie hier beschrieben:
#   https://www.pygame.org/docs/ref/mouse.html?highlight=left
#
def main():
   done = False                # zeigt ob Spiel aus ist.
   while not done:
        for event in pygame.event.get():
            # This block is executed once for each MOUSEBUTTONDOWN event.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    for button in button_list:
                        # `event.pos` is the mouse position.
                        if button['rect'].collidepoint(event.pos):
                            # Increment the number by calling the callback
                            # function in the button list.
                            button['callback']()
                # Erst einmal die Position des Mausklicks festhalten
                (x,y) = pygame.mouse.get_pos()  
                # Wenn die vertikale und horizontale Position stimmt:
                if y >= s1.posKarteny and x > 10 and x < 620:
                      x1 = (x - s1.posKartenx) // k.abstandKartenX
                      # Die letzte Karte bekommt eine Sonderbehandlung:
                      if x1 == 8:
                         x1 = 7
                      # Prüfen welche Karte angeklickt wurde
                      if event.button == 1: # Linke Maustaste
                         action = s1.legeKarteAus(s1.handkarten[x1])
                      elif event.button == 3: # Rechte Maustaste
                         action = s1.legeAufAbwurfstapel(s1.handkarten[x1])
                      # Wenn der Spieler was getan hat ist der Computer an der
                      # Reihe
                      if action:
                          (aktion, kk) = s2.waehleKarte()
                          # Bei der Aktion gibt es "ausspielen" und "ablegen"
                          if aktion == "ausspielen":
                             s2.legeKarteAus(kk)
                          elif aktion == "ablegen":
                             s2.legeAufAbwurfstapel(kk)
                          else:
                              print("Hier dar er nicht hinkommen!")
                      if len(s.talon) == 0:
                          print("Talon ist leer")
                          s.spielEnde()
                          done = True

   while done:
     for event in pygame.event.get():
       if event.type == pygame.MOUSEBUTTONDOWN:
       # 1 is the left mouse button, 2 is middle, 3 is right.
         if event.button == 1:
           for button in button_list:
             # `event.pos` is the mouse position.
             if button['rect'].collidepoint(event.pos):
               # Increment the number by calling the callback
               # function in the button list.
               button['callback']()

main()
