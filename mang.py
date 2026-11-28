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
        self.kuva = pygame.Surface((320, 180))
        self.kell = pygame.time.Clock()
        self.liikumine = [False, False] 

        self.varad = {
            #"dekoratsioonid": lae_pildid("tee_piltideni") # dekoratsioonide jaoks
            "korter_punane": lae_pildid("keskkond/korterid/punane"), # korterite ruudud
            "korter_sinine": lae_pildid("keskkond/korterid/sinine"),
            "korter_klaas": lae_pildid("keskkond/korterid/klaas"),
            "tee": lae_pildid("keskkond/tee"), # tee erinevad ruudud
            "veetorn": lae_pildid("keskkond/propid/veetorn"),
            "veetorn_fuusiline": lae_pildid("keskkond/propid/veetorn/fuusiline"),
            "propid": lae_pildid("keskkond/propid"),
            "tootorn_fuusiline": lae_pildid("keskkond/propid/fuusiline"),
            "mangija": lae_pilt("mängija/vara/paigal_seisev/Sprite-0003.png"),
            "mangija/paigal_seisev": Animatsioon(lae_pildid("mängija/vara/paigal_seisev"), pilt_kestus=6),
            "mangija/kõndimine": Animatsioon(lae_pildid("mängija/vara/kõndimine"), pilt_kestus=6),
            "mangija/jooksmine": Animatsioon(lae_pildid("mängija/vara/jooksmine"), pilt_kestus=4),
            "mangija/hüppamine": Animatsioon(lae_pildid("mängija/vara/hüppamine"), pilt_kestus=10),
            "mangija/palvetamine": Animatsioon(
                [lae_pilt(f"mängija/vara/palvetamine/praying{i}.png") for i in range(1, 15)],
                pilt_kestus=6,
                loop=False,
            ),

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
                    if sundmus.key == pygame.K_a:
                        self.liikumine[0] = True
                    if sundmus.key == pygame.K_d:
                        self.liikumine[1] = True
                    if sundmus.key == pygame.K_w:
                        self.mangija.kiirus[1] = -3.5
                    if sundmus.key == pygame.K_m:
                        self.mangija.meditatsioon = True
                if sundmus.type == pygame.KEYUP:
                    if sundmus.key == pygame.K_a:
                        self.liikumine[0] = False
                    if sundmus.key == pygame.K_d:
                        self.liikumine[1] = False
            
            # Aseta renderimis jerjekorras asjad, taust koige enne ja asjad selle peale, jne.
            self.kuva.fill((50, 58, 94))
            self.kuva.fill((135, 206, 250))
            self.ruudu_kaart.render(self.kuva, nihe=self.kerimine)

            self.kerimine[0] += (self.mangija.rect().centerx - self.kuva.get_width() / 2 - self.kerimine[0]) / 30
            self.kerimine[1] += (self.mangija.rect().centery - self.kuva.get_height() / 2 - self.kerimine[1]) / 30

            self.mangija.update((self.liikumine[1] - self.liikumine[0], 0))
            self.mangija.esitus(self.kuva, nihe=self.kerimine)
            

            self.ekraan.blit(pygame.transform.scale(self.kuva, self.ekraan.get_size()), (0, 0))
            pygame.display.update()
            self.kell.tick(60)


Mang().kaivita()
