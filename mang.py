import sys
import pygame

from koodifailid.kommud import lae_pilt, lae_pildid
from koodifailid.ruudukaart import  Ruudukaart

class Mang:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Mäng")

        self.ekraan = pygame.display.set_mode((640*2, 360*2))
        self.kuva = pygame.Surface((320, 180))
        self.kell = pygame.time.Clock()

        self.varad = {
            #"dekoratsioonid": lae_pildid("tee_piltideni") # dekoratsioonide jaoks
            "korter_punane": lae_pildid("keskkond/korterid/punane"), # korterite ruudud
            "tee": lae_pildid("keskkond/tee"), # tee erinevad ruudud
        }

        self.ruudu_kaart = Ruudukaart(self, ruudu_suurus=16)
    
    def kaivita(self):
        while True:
            for sundmus in pygame.event.get():
                if sundmus.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Aseta renderimis jerjekorras asjad, taust koige enne ja asjad selle peale, jne.
            self.kuva.fill((20, 20, 30))
            self.ruudu_kaart.render(self.kuva)

            # Ekraani zoom
            self.ekraan.blit(pygame.transform.scale(self.kuva, self.ekraan.get_size()), (0, 0))

            pygame.display.update()
            self.kell.tick(60)


Mang().kaivita()


