import pygame
from koodifailid import ruudukaart as ruudukaart

HITBOX_X_OFFSET = 8

class Fyysika:
    def __init__(self, mang, e_tyyp, pos, suurus):
        self.mang = mang
        self.e_tyyp = e_tyyp
        self.tyyp = e_tyyp
        self.tegevus = None
        self.pos = list(pos)
        self.suurus = suurus
        self.kiirus = [0, 0]
        self.kokkuporked = {'yles': False, 'alla': False, 'parem' : False, 'vasak' : False}

        self.action = ''
        self.anim_offset = (-3, 0)
        self.flip = False
        self.lisa_tegevus('paigal_seisev')

    def rect(self):
        return pygame.Rect(self.pos[0] + HITBOX_X_OFFSET, self.pos[1], self.suurus[0], self.suurus[1])


    def lisa_tegevus(self, tegevus):
        if getattr(self, "tegevus", None) != tegevus:
            self.tegevus = tegevus
            self.animatsioon = self.mang.varad[self.tyyp + '/' + self.tegevus].copy()


    def kokkuporke_ruudud(self, entity_rect):
        kontrolli_positsioonid = (
            (entity_rect.left, entity_rect.top),
            (entity_rect.right - 1, entity_rect.top),
            (entity_rect.left, entity_rect.bottom - 1),
            (entity_rect.right - 1, entity_rect.bottom - 1),
        )
        ruudud = []
        for pos in kontrolli_positsioonid:
            ruudud.extend(self.mang.ruudu_kaart.fuusilised_ruudud_umberringi(pos))
        return [ruut for ruut in ruudud if entity_rect.colliderect(ruut)]

    def update(self, liikumine=(0, 0)):
        for suund in self.kokkuporked:
            self.kokkuporked[suund] = False

        self.kiirus[1] = min(5, self.kiirus[1] + 0.1)
        liikumine_x = liikumine[0] + self.kiirus[0]
        liikumine_y = liikumine[1] + self.kiirus[1]

        self.pos[0] += liikumine_x
        entity_rect = self.rect()
        kokkuporked = self.kokkuporke_ruudud(entity_rect)
        if kokkuporked and liikumine_x > 0:
            self.kokkuporked['parem'] = True
            entity_rect.right = min(ruut.left for ruut in kokkuporked)
            self.pos[0] = entity_rect.x - HITBOX_X_OFFSET
            self.kiirus[0] = 0
        elif kokkuporked and liikumine_x < 0:
            self.kokkuporked['vasak'] = True
            entity_rect.left = max(ruut.right for ruut in kokkuporked)
            self.pos[0] = entity_rect.x - HITBOX_X_OFFSET
            self.kiirus[0] = 0

        self.pos[1] += liikumine_y
        entity_rect = self.rect()
        kokkuporked = self.kokkuporke_ruudud(entity_rect)
        if kokkuporked and liikumine_y > 0:
            self.kokkuporked['alla'] = True
            entity_rect.bottom = min(ruut.top for ruut in kokkuporked)
            self.pos[1] = entity_rect.y
            self.kiirus[1] = 0
        elif kokkuporked and liikumine_y < 0:
            self.kokkuporked['yles'] = True
            entity_rect.top = max(ruut.bottom for ruut in kokkuporked)
            self.pos[1] = entity_rect.y
            self.kiirus[1] = 0

        if liikumine_y >= 0 and self.kokkuporke_ruudud(entity_rect.move(0, 1)):
            self.kokkuporked['alla'] = True

        if liikumine[0] > 0:
            self.flip = False
        if liikumine[0] < 0:
            self.flip = True

        if self.tegevus != 'hüppamine' or self.kiirus[1] <= 0:
            self.animatsioon.update()

    def esitus(self, pind, nihe=(0, 0)):
        nihe_x, nihe_y = int(nihe[0]), int(nihe[1])
        pilt = self.animatsioon.pilt()
        pildi_y = self.pos[1] - nihe[1] + self.suurus[1] - pilt.get_height() + self.anim_offset[1]
        pind.blit(pygame.transform.flip(pilt, self.flip, False), (self.pos[0] - nihe[0] + self.anim_offset[0], pildi_y))
        #pind.blit(self.mang.varad["mangija"], (self.pos[0] - nihe_x, self.pos[1] - nihe_y))


class Mangija(Fyysika):
    KONDISE_KUNI_JOOKS = 20
    KONDI_KIIRUS = 1
    JOOKSMISE_KIIRUS = 2

    def __init__(self, mang, pos, suurus):
        super().__init__(mang, "mangija", pos, suurus)
        self.ohu_aeg = 0
        self.liikumise_aeg = 0


    def update(self, liikumine=(0, 0)):
        if liikumine[0] != 0:
            self.liikumise_aeg += 1
        else:
            self.liikumise_aeg = 0

        if self.liikumise_aeg >= self.KONDISE_KUNI_JOOKS:
            liikumiskiirus = self.JOOKSMISE_KIIRUS
        else:
            liikumiskiirus = self.KONDI_KIIRUS
        super().update(liikumine=(liikumine[0] * liikumiskiirus, liikumine[1]))

        self.ohu_aeg += 1
        if self.kokkuporked['alla']:
            self.ohu_aeg = 0

        if self.ohu_aeg > 4:
            self.lisa_tegevus('hüppamine')
        elif liikumine[0] != 0:
            if self.liikumise_aeg >= self.KONDISE_KUNI_JOOKS:
                self.lisa_tegevus('jooksmine')
            else:
                self.lisa_tegevus('kõndimine')
        else:
            self.lisa_tegevus('paigal_seisev')
