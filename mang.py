import sys
import pygame

from koodifailid.kommud import lae_pilt, lae_pildid
from koodifailid.ruudukaart import  Ruudukaart

class Mang:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Mäng")

        self.ekraan = pygame.display.set_mode((640, 480))
        self.kuva = pygame.Surface((320, 240))
        self.kell = pygame.time.Clock()

        self.varad = {
            #"dekoratsioonid": lae_pildid("tee_piltideni") # dekoratsioonide jaoks
            "korter_punane": lae_pildid("keskkond/korterid/punane"), # korterite ruudud
            "tee": lae_pildid("keskkond/tee"), # tee erinevad ruudud
        }
        #self.pilt = pygame.image.load("tee_failini")

        self.ruudu_kaart = Ruudukaart(self, ruudu_suurus=16)
    
    def kaivita(self):
        while True:
            for sundmus in pygame.event.get():
                if sundmus.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Aseta renderimis jerjekorras asjad, taust koige enne ja asjad selle peale, jne.
            self.ekraan.fill((20, 20, 30))
            self.ruudu_kaart.render(self.ekraan)

            self.kuva.blit(pygame.transform.scale(self.ekraan, self.kuva.get_size()), (0, 0))

            pygame.display.update()
            self.kell.tick(60)


Mang().kaivita()


