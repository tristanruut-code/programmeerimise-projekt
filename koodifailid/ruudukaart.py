import pygame

NAABER_NIHE = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
FUUSILISED_RUUDUD = {"korterid", "tee"} # Ruudu tyyp mida me tahame et oleks collisioniga

class Ruudukaart:
    def __init__(self, mang, ruudu_suurus=16):
        self.mang = mang
        self.ruudu_suurus = ruudu_suurus
        self.ruudu_kaart = {}
        self.vabad_ruudud = []

        for i in range(10):
            self.ruudu_kaart[str(3 + i) + ";10"] = {"tuup": "korterid", "variant": 1, "pos": (3 + i, 10)}
            self.ruudu_kaart["10;" + str(5 + i)] = {"tuup": "tee", "variant": 1, "pos": (10, i + 5)}
    
    def ruudud_umberingi(self, pos):
        ruudud = []
        ruudu_koht = (int(pos[0] // self.ruudu_suurus)), (int(pos[1] // self.ruudu_suurus))
        for nihe in NAABER_NIHE:
            kontrolli_koht = str(ruudu_koht[0] + nihe[0]) + ";" + str(ruudu_koht[1] + nihe[1])
            if kontrolli_koht in self.ruudu_kaart:
                ruudud.append(self.ruudu_kaart[kontrolli_koht])
        return ruudud
    
    def fuusilised_ruudud_umberringi(self, pos):
        ruudud = []
        for ruut in self.ruudud_umberingi(pos):
            if ruut["tuup"] in FUUSILISED_RUUDUD:
                ruudud.append(pygame.Rect(ruut["pos"][0] * self.ruudu_suurus, ruut["pos"] * self.ruudu_suurus, self.ruudu_suurus, self.ruudu_suurus))
        return ruudud
 
    def render(self, pind):
        for ruut in self.vabad_ruudud:
            pind.blit(self.mang.varad[ruut["tuup"]][ruut["variant"]], ruut["pos"])
        
        for koht in self.ruudu_kaart:
            ruut = self.ruudu_kaart[koht]
            pind.blit(self.mang.varad[ruut["tuup"]][ruut["variant"]], (ruut["pos"][0] * self.ruudu_suurus, ruut["pos"][1] * self.ruudu_suurus))
        