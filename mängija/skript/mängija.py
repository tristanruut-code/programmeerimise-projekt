import pygame
class Fyysika:
    def __init__(self, mang, e_tyyp, pos, suurus):
        self.mang = mang
        self.e_tyyp = e_tyyp
        self.pos = list(pos)
        self.suurus = suurus
        self.kiirus = [0, 0]



    def update(self, liikumine=(0, 0)):
        kaadri_liikumine = (liikumine[0] + self.kiirus[0], liikumine[1] + self.kiirus[1])

        self.pos[0] += kaadri_liikumine[0]
        self.pos[1] += kaadri_liikumine[1]

    def esitus(self, pind):
        pind.blit(self.mang.varad["mangija"], (self.pos[0], self.pos[1]))