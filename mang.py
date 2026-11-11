import sys
import pygame
from mängija.skript.mängija import Fyysika

from koodifailid.kommud import lae_pilt, lae_pildid
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
            "mangija": lae_pilt("mängija/vara/paigal_seisev/Sprite-0003.png")
        }

        self.ruudu_kaart = Ruudukaart(self, ruudu_suurus=16)
        self.mangija = Fyysika(self, 'mängija', (50, 50), (16, 32))

        self.ruudu_kaart = Ruudukaart(self, ruudu_suurus=16)
        try:
            self.ruudu_kaart.lae("linn.json")
        except FileNotFoundError:
            pass
    
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
                if sundmus.type == pygame.KEYUP:
                    if sundmus.key == pygame.K_LEFT:
                        self.liikumine[0] = False
                    if sundmus.key == pygame.K_RIGHT:
                        self.liikumine[1] = False
            
            # Aseta renderimis jerjekorras asjad, taust koige enne ja asjad selle peale, jne.
            self.kuva.fill((20, 20, 30))
            self.ruudu_kaart.render(self.kuva)

            self.mangija.update((self.liikumine[1] - self.liikumine[0], 0))
            self.mangija.esitus(self.kuva)
            

            self.ekraan.blit(pygame.transform.scale(self.kuva, self.ekraan.get_size()), (0, 0))
            pygame.display.update()
            self.kell.tick(60)


Mang().kaivita()


