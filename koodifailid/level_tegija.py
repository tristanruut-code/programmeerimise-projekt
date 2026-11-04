import sys
import pygame

from kommud import lae_pildid
from ruudukaart import  Ruudukaart

class LevelTegija:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Leveli Tegija")

        self.ekraan = pygame.display.set_mode((640*2, 360*2))
        self.kuva = pygame.Surface((320, 180))
        self.kell = pygame.time.Clock()

        self.varad = {
            "korter_punane": lae_pildid("keskkond/korterid/punane"),
            "korter_sinine": lae_pildid("keskkond/korterid/sinine"), # korterite ruudud
            "tee": lae_pildid("keskkond/tee"), # tee erinevad ruudud
        }

        self.liikumine = [False, False, False, False]

        self.ruudu_kaart = Ruudukaart(self, ruudu_suurus=16)

        self.kerimine = [0, 0]

        self.ruudu_list = list(self.varad)
        self.ruudu_grupp = 0
        self.ruudu_variant = 0
    
        self.clicking = False
        self.right_clicking = False
        self.shift = False

    def kaivita(self):
        while True:
            for sundmus in pygame.event.get():
                if sundmus.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if sundmus.type == pygame.MOUSEBUTTONDOWN:
                    if sundmus.button == 1:
                        self.clicking = True
                    if sundmus.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if sundmus.button == 4:
                            self.ruudu_variant = (self.ruudu_variant - 1) % len(self.varad[self.ruudu_list[self.ruudu_grupp]])
                        if sundmus.button == 5:
                            self.ruudu_variant = (self.ruudu_variant + 1) % len(self.varad[self.ruudu_list[self.ruudu_grupp]])
                    else:
                        if sundmus.button == 4:
                            self.ruudu_grupp = (self.ruudu_grupp - 1) % len(self.ruudu_list)
                            self.ruudu_variant = 0
                        if sundmus.button == 5:
                            self.ruudu_grupp = (self.ruudu_grupp + 1) % len(self.ruudu_list)
                            self.ruudu_variant = 0
                if sundmus.type == pygame.MOUSEBUTTONUP:
                    if sundmus.button == 1:
                        self.clicking = False
                    if sundmus.button == 3:
                        self.right_clicking = False

                if sundmus.type == pygame.KEYDOWN:
                    if sundmus.key == pygame.K_LEFT:
                        self.liikumine[0] = True
                    if sundmus.key == pygame.K_RIGHT:
                        self.liikumine[1] = True
                    if sundmus.key == pygame.K_UP:
                        self.liikumine[2] = True
                    if sundmus.key == pygame.K_DOWN:
                        self.liikumine[3] = True
                    if sundmus.key == pygame.K_LSHIFT:
                        self.shift = True
                if sundmus.type == pygame.KEYUP:
                    if sundmus.key == pygame.K_LEFT:
                        self.liikumine[0] = False
                    if sundmus.key == pygame.K_RIGHT:
                        self.liikumine[1] = False
                    if sundmus.key == pygame.K_UP:
                        self.liikumine[2] = False
                    if sundmus.key == pygame.K_DOWN:
                        self.liikumine[3] = False 
                    if sundmus.key == pygame.K_LSHIFT:
                        self.shift = False
            
            # Aseta renderimis jerjekorras asjad, taust koige enne ja asjad selle peale, jne.
            self.kuva.fill((20, 20, 30))

            render_kerimine = (int(self.kerimine[0]), int(self.kerimine[1]))

            self.ruudu_kaart.render(self.kuva, nihe=self.kerimine)

            praegune_ruudu_pilt = self.varad[self.ruudu_list[self.ruudu_grupp]][self.ruudu_variant].copy()
            praegune_ruudu_pilt.set_alpha(100)

            hpos = pygame.mouse.get_pos()
            hpos = (
                hpos[0] * self.kuva.get_width() / self.ekraan.get_width(),
                hpos[1] * self.kuva.get_height() / self.ekraan.get_height(),
            )
            ruudu_pos = (int((hpos[0] + self.kerimine[0]) // self.ruudu_kaart.ruudu_suurus), int((hpos[1] + self.kerimine[1]) // self.ruudu_kaart.ruudu_suurus))

            if self.clicking:
                self.ruudu_kaart.ruudu_kaart[str(ruudu_pos[0]) + ";" + str(ruudu_pos[1])] = {"tuup": self.ruudu_list[self.ruudu_grupp], "variant": self.ruudu_variant, "pos": ruudu_pos}

            self.kuva.blit(praegune_ruudu_pilt, (5, 5))

            self.ekraan.blit(pygame.transform.scale(self.kuva, self.ekraan.get_size()), (0, 0))

            pygame.display.update()
            self.kell.tick(60)


LevelTegija().kaivita()


