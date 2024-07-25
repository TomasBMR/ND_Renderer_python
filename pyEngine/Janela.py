import pygame
from .Quadro import Quadro

class Janela:
    # Aqui vai acontecer a 
    #Eventualmente mudar cena para cenas ou *cenas
    def __init__(self, largura, altura, nome=None, cor_fundo=(200, 150, 50)):
        self.largura = largura
        self.altura = altura
        #self.cena = cena #Talvez seja interessante receber gerenciador no futuro

        self.cor_fundo = cor_fundo

        pygame.init()
        self.tela: pygame.Surface = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption(nome)

    def Draw(self, quadros:list[Quadro]):
        self.tela.fill(self.cor_fundo)
        #Mudar a forma de reescalar, talvez passando janela como argumento para cena
        for quadro in quadros:
            #img = pygame.transform.scale(fig, (self.largura, self.altura))
            fig, pos = quadro.getSurfnPos()
            self.tela.blit(fig, pos)
        pygame.display.update()

    def get_proporcao(self):
        return self.altura, self.largura

"""Escrever uma classe "wrapper" para pygame surface para facilitar o desenho de imagens a janela
algo como
class Quadro:
    def __init__(self, surf:pygame.Surface, pos:tuple[int, int], largura: int, altura: int):
        self.surf: pygame.Surface = surf
        self.pos: np.ndarray = pos
        self.largura: int = largura
        self.altura: int = altura
        #self.transparencia??
    def getSurfnPos(self):
        return self.surf, self.pos
"""
   