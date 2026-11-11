import os
import pygame

def lae_pilt(tee):
    pilt = pygame.image.load(tee).convert()
    pilt.set_colorkey((0, 0, 0))
    return pilt

def lae_pildid(tee):
    pildid = []
    for pildi_nimi in sorted(os.listdir(tee)):
        pildid.append(lae_pilt(tee + "/" + pildi_nimi))
    return pildid

class Animatsioon:
    def __init__(self, pildid, pilt_kestus=5, loop=True):
        self.pildid = pildid
        self.loop = loop
        self.pilt_kestus = pilt_kestus
        self.done = False
        self.kaader = 0

    def copy(self):
        return Animatsioon(self.pildid, self.pilt_kestus, self.loop)

    def update(self):
        if self.loop:
            self.kaader = (self.kaader + 1) % (self.pilt_kestus * len(self.pildid))
        else:
            self.kaader = min(self.kaader + 1, self.pilt_kestus * len(self.pildid) - 1)
            if self.kaader >= self.pilt_kestus * len(self.pildid) - 1:
                self.done = True



    def pilt(self):
        return self.pildid[int(self.kaader / self.pilt_kestus)]