import pygame
import json

# 3x3 komplekt: 00-08 rida-realt. Võti = millistel külgedel on sama tüüpi naaber.
AUTO_TILE_ARV = 9
KORTER_KAART = {
    frozenset([(1, 0), (0, 1)]): 0, # ülemine vasak nurk
    frozenset([(-1, 0), (1, 0), (0, 1)]): 1,  # ülemine serv
    frozenset([(-1, 0), (0, 1)]): 2, # ülemine parem nurk
    frozenset([(0, -1), (0, 1), (1, 0)]): 3, # vasak serv
    frozenset([(-1, 0), (1, 0), (0, -1), (0, 1)]): 4, # keskmine
    frozenset([(0, -1), (0, 1), (-1, 0)]): 5, # parem serv
    frozenset([(1, 0), (0, -1)]): 6, # alumine vasak nurk
    frozenset([(-1, 0), (1, 0), (0, -1)]): 7, # alumine serv
    frozenset([(-1, 0), (0, -1)]): 8, # alumine parem nurk
}
# variandid, mis ei loe seina naabriks (rõdu piire jne)
EI_NAABER = {
    "korter_punane": {10, 11},
    "korter_sinine": {11},
}

def korter_variant(naabrid):
    return KORTER_KAART.get(frozenset(naabrid), 9)

def tee_variant(naabrid):
    vasak = (-1, 0) in naabrid
    parem = (1, 0) in naabrid
    ules = (0, -1) in naabrid

    if parem and not vasak:
        veerg = 0
    elif vasak and not parem:
        veerg = 2
    else:
        veerg = 1

    rida = 1 if ules else 0
    return rida * 3 + veerg

# tüüp: (variandi-funktsioon, auto-tile'ide arv)
AUTO_TUUBID = {
    "korter_punane": (korter_variant, 4),
    "korter_sinine": (korter_variant, 9),
    "tee": (tee_variant, 6),
}

NAABER_NIHE = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
FUUSILISED_RUUDUD = {"tee", "korter_punane", "korter_sinine", "veetorn_fuusiline"} # Ruudu tyyp mida me tahame et oleks collisioniga
AUTO_PAIGUTAMISE_RUUDUD = {"tee", "korter_punane", "korter_sinine"}

class Ruudukaart:
    def __init__(self, mang, ruudu_suurus=16):
        self.mang = mang
        self.ruudu_suurus = ruudu_suurus
        self.ruudu_kaart = {}
        self.vabad_ruudud = []

    def ruudud_umberringi(self, pos):
        ruudud = []
        ruudu_koht = (int(pos[0] // self.ruudu_suurus)), (int(pos[1] // self.ruudu_suurus))
        for nihe in NAABER_NIHE:
            kontrolli_koht = str(ruudu_koht[0] + nihe[0]) + ";" + str(ruudu_koht[1] + nihe[1])
            if kontrolli_koht in self.ruudu_kaart:
                ruudud.append(self.ruudu_kaart[kontrolli_koht])
        return ruudud
    
    def salvesta(self, tee):
        with open(tee, "w") as fail:
            json.dump({"ruudu_kaart": self.ruudu_kaart, "ruudu_suurus": self.ruudu_suurus, "vabad_ruudud": self.vabad_ruudud}, fail)
    
    def lae(self, tee):
        with open(tee, "r") as fail:
            kaardi_andmed = json.load(fail)
        
        self.ruudu_kaart = kaardi_andmed["ruudu_kaart"]
        self.ruudu_suurus = kaardi_andmed["ruudu_suurus"]
        self.vabad_ruudud = kaardi_andmed["vabad_ruudud"]

    def fuusilised_ruudud_umberringi(self, pos):
        ruudud = []
        for ruut in self.ruudud_umberringi(pos):
            if ruut["tuup"] in FUUSILISED_RUUDUD:
                ruudud.append(pygame.Rect(ruut["pos"][0] * self.ruudu_suurus, ruut["pos"][1] * self.ruudu_suurus, self.ruudu_suurus, self.ruudu_suurus))
        return ruudud

    def autopaigutamine(self):
        for ruut in self.ruudu_kaart.values():
            andmed = AUTO_TUUBID.get(ruut["tuup"])
            if not andmed:
                continue
            variandi_fn, arv = andmed
            if ruut["variant"] >= arv:
                continue  # käsitsi pandud tile

            naabrid = set()
            for nihe in ((1, 0), (-1, 0), (0, -1), (0, 1)):
                koht = str(ruut["pos"][0] + nihe[0]) + ";" + str(ruut["pos"][1] + nihe[1])
                naaber = self.ruudu_kaart.get(koht)
                if (naaber and naaber["tuup"] == ruut["tuup"] and naaber["variant"] not in EI_NAABER.get(ruut["tuup"], ())):
                    naabrid.add(nihe)

            ruut["variant"] = variandi_fn(naabrid)

    def render(self, pind, nihe=(0, 0)):
        nihe_x, nihe_y = int(nihe[0]), int(nihe[1])
        for ruut in self.vabad_ruudud:
            pind.blit(self.mang.varad[ruut["tuup"]][ruut["variant"]], (ruut["pos"][0] - nihe_x, ruut["pos"][1] - nihe_y))
        
        for x in range(nihe_x // self.ruudu_suurus, (nihe_x + pind.get_width()) // self.ruudu_suurus + 1):
            for y in range(nihe_y // self.ruudu_suurus, (nihe_y + pind.get_height()) // self.ruudu_suurus + 1):
                asukoht = str(x) + ";" + str(y)
                if asukoht in self.ruudu_kaart:
                    ruut = self.ruudu_kaart[asukoht]
                    pind.blit(
                        self.mang.varad[ruut["tuup"]][ruut["variant"]],
                        (ruut["pos"][0] * self.ruudu_suurus - nihe_x, ruut["pos"][1] * self.ruudu_suurus - nihe_y),
                    )