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

        try:
            self.ruudu_kaart.lae("linn.json")
        except FileNotFoundError:
            pass

        self.kerimine = [0, 0]

        self.ruudu_list = list(self.varad)
        self.ruudu_grupp = 0
        self.ruudu_variant = 0
    
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ruudustikus = True

    def kaivita(self):
        while True:
            for sundmus in pygame.event.get():
                if sundmus.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if sundmus.type == pygame.MOUSEBUTTONDOWN:
                    if sundmus.button == 1:
                        self.clicking = True
                        if not self.ruudustikus:
                            self.ruudu_kaart.vabad_ruudud.append({"tuup": self.ruudu_list[self.ruudu_grupp], "variant": self.ruudu_variant, "pos": (hpos[0] + self.kerimine[0], hpos[1] + self.kerimine[1])})
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
                    if sundmus.key == pygame.K_a:
                        self.liikumine[0] = True
                    if sundmus.key == pygame.K_d:
                        self.liikumine[1] = True
                    if sundmus.key == pygame.K_w:
                        self.liikumine[2] = True
                    if sundmus.key == pygame.K_s:
                        self.liikumine[3] = True
                    if sundmus.key == pygame.K_g:
                        self.ruudustikus = not self.ruudustikus
                    if sundmus.key == pygame.K_s and (sundmus.mod & pygame.KMOD_CTRL):
                        self.ruudu_kaart.salvesta("linn.json")
                    if sundmus.key == pygame.K_t:
                        self.ruudu_kaart.autopaigutamine()
                    if sundmus.key == pygame.K_LSHIFT:
                        self.shift = True
                if sundmus.type == pygame.KEYUP:
                    if sundmus.key == pygame.K_a:
                        self.liikumine[0] = False
                    if sundmus.key == pygame.K_d:
                        self.liikumine[1] = False
                    if sundmus.key == pygame.K_w:
                        self.liikumine[2] = False
                    if sundmus.key == pygame.K_s:
                        self.liikumine[3] = False
                    if sundmus.key == pygame.K_LSHIFT:
                        self.shift = False
            
            # Aseta renderimis jerjekorras asjad, taust koige enne ja asjad selle peale, jne.
            self.kuva.fill((255, 255, 255))

            self.kerimine[0] += (self.liikumine[1] - self.liikumine[0]) * 4
            self.kerimine[1] += (self.liikumine[3] - self.liikumine[2]) * 4
            render_kerimine = (int(self.kerimine[0]), int(self.kerimine[1]))

            self.ruudu_kaart.render(self.kuva, nihe=self.kerimine)

            praegune_ruudu_pilt = self.varad[self.ruudu_list[self.ruudu_grupp]][self.ruudu_variant].copy()
            praegune_ruudu_pilt.set_alpha(200)

            hpos = pygame.mouse.get_pos()
            hpos = (
                hpos[0] * self.kuva.get_width() / self.ekraan.get_width(),
                hpos[1] * self.kuva.get_height() / self.ekraan.get_height(),
            )
            ruudu_pos = (int((hpos[0] + self.kerimine[0]) // self.ruudu_kaart.ruudu_suurus), int((hpos[1] + self.kerimine[1]) // self.ruudu_kaart.ruudu_suurus))

            if self.ruudustikus:
                self.kuva.blit(praegune_ruudu_pilt, (ruudu_pos[0] * self.ruudu_kaart.ruudu_suurus - self.kerimine[0], ruudu_pos[1] * self.ruudu_kaart.ruudu_suurus - self.kerimine[1]))
            else:
                self.kuva.blit(praegune_ruudu_pilt, hpos)

            if self.clicking and self.ruudustikus:
                self.ruudu_kaart.ruudu_kaart[str(ruudu_pos[0]) + ";" + str(ruudu_pos[1])] = {"tuup": self.ruudu_list[self.ruudu_grupp], "variant": self.ruudu_variant, "pos": ruudu_pos}
            if self.right_clicking:
                ruudu_koht = str(ruudu_pos[0]) + ";" + str(ruudu_pos[1])
                if ruudu_koht in self.ruudu_kaart.ruudu_kaart:
                    del self.ruudu_kaart.ruudu_kaart[ruudu_koht]
                for ruut in self.ruudu_kaart.vabad_ruudud.copy():
                    ruudu_pilt = self.varad[ruut["tuup"], ruut["variant"]]
                    ruudu_r = pygame.Rect(ruut["pos"][0] - self.kerimine[0], ruut["pos"][1] - self.kerimine[1], ruudu_pilt.get_width(), ruudu_pilt.get_height())
                    if ruudu_r.collidepoint(hpos):
                        self.ruudu_kaart.vabad_ruudud.remove(ruut)

            self.kuva.blit(praegune_ruudu_pilt, (5, 5))

            self.ekraan.blit(pygame.transform.scale(self.kuva, self.ekraan.get_size()), (0, 0))

            pygame.display.update()
            self.kell.tick(60)


LevelTegija().kaivita()


