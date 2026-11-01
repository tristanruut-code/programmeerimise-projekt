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