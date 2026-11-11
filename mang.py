import sys
import pygame
from mängija.skript.mängija import Fyysika, Mangija
from koodifailid.kommud import lae_pilt, lae_pildid, Animatsioon
from koodifailid.ruudukaart import  Ruudukaart

class Mang:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Mäng")

        self.ekraan = pygame.display.set_mode((640*2, 360*2))
        self.kuva = pygame.Surface((480, 270))
        self.kell = pygame.time.Clock()
        self.liikumine = [False, False] 

        self.varad = {
            #"dekoratsioonid": lae_pildid("tee_piltideni") # dekoratsioonide jaoks
            "korter_punane": lae_pildid("keskkond/korterid/punane"), # korterite ruudud
            "korter_sinine": lae_pildid("keskkond/korterid/sinine"),
            "tee": lae_pildid("keskkond/tee"), # tee erinevad ruudud
            "mangija": lae_pilt("mängija/vara/paigal_seisev/Sprite-0003.png"),
            "mangija/paigal_seisev": Animatsioon(lae_pildid("mängija/vara/paigal_seisev"), pilt_kestus=6),
            "mangija/kõndimine": Animatsioon(lae_pildid("mängija/vara/kõndimine"), pilt_kestus=6),
            "mangija/jooksmine": Animatsioon(lae_pildid("mängija/vara/jooksmine"), pilt_kestus=4),
            "mangija/hüppamine": Animatsioon(lae_pildid("mängija/vara/hüppamine"), pilt_kestus=10),

        }

        self.ruudu_kaart = Ruudukaart(self, ruudu_suurus=16)
        self.mangija = Mangija(self, (96, 32), (16, 32))

        self.ruudu_kaart = Ruudukaart(self, ruudu_suurus=16)
        try:
            self.ruudu_kaart.lae("linn.json")
        except FileNotFoundError:
            pass

        self.kerimine = [0, 0]
    
    def kaivita(self):
        while True:
            for sundmus in pygame.event.get():
                if sundmus.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if sundmus.type == pygame.KEYDOWN:
                    if sundmus.key == pygame.K_LEFT:
                        self.liikumine[0] = True
                    if sundmus.key == pygame.K_RIGHT:
                        self.liikumine[1] = True
                    if sundmus.key == pygame.K_UP:
                        self.mangija.kiirus[1] = -3
                if sundmus.type == pygame.KEYUP:
                    if sundmus.key == pygame.K_LEFT:
                        self.liikumine[0] = False
                    if sundmus.key == pygame.K_RIGHT:
                        self.liikumine[1] = False
            
            # Aseta renderimis jerjekorras asjad, taust koige enne ja asjad selle peale, jne.
            self.kuva.fill((120, 120, 120))
            self.ruudu_kaart.render(self.kuva, nihe=self.kerimine)

            self.kerimine[0] += (self.mangija.rect().centerx - self.kuva.get_width() / 2 - self.kerimine[0]) / 30
            self.kerimine[1] += (self.mangija.rect().centery - self.kuva.get_height() / 2 - self.kerimine[1]) / 30

            self.mangija.update((self.liikumine[1] - self.liikumine[0], 0))
            self.mangija.esitus(self.kuva, nihe=self.kerimine)
            

            self.ekraan.blit(pygame.transform.scale(self.kuva, self.ekraan.get_size()), (0, 0))
            pygame.display.update()
            self.kell.tick(60)


Mang().kaivita()
