import pygame

class Quadro:
    def __init__(self, surf:pygame.Surface, largura: int=None, altura: int=None, pos:tuple[int, int]=(0,0)):
        self.surf: pygame.Surface = surf
        self.largura: int = largura if largura!=None else surf.get_width()
        self.altura: int = altura if altura!=None else surf.get_height()
        self.pos: tuple[int, int] = pos
        #self.transparencia??

    def getSurfnPos(self):
        return self.surf, self.pos
    
    def setSurf(self, surf):
        self.surf = surf

    def blit(self, quad):
        self.surf.blit(quad.surf, quad.pos)
   
    #Escrever um set Surf q leve em conta a escala