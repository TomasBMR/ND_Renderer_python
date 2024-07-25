import pygame, time, sys

from .Janela import Janela
from .GUI import GUIManager, GUI
from .Quadro import Quadro
from .Cena import Cena


class Gerenciador():
    def __init__(self, largura: int, altura: int, cena: type[Cena]):
        self.largura: int = largura
        self.altura: int = altura

        self.janela: Janela = Janela(self.largura, self.altura, "3D Renderer", cor_fundo=(24, 68, 112))
        self.guiManager: GUIManager  = GUIManager()

        #objs vai ter mudar
        self.cena: Cena = cena(largura, altura, self.guiManager)
        self.cenas: list[Cena] = [cena] #MainCena(largura, altura, self.guiManager)]

        self.font = pygame.font.SysFont("Arial", 18)
        self.clock = pygame.time.Clock()
        self.framerate = 120


    def Input(self):
         #isso talvez caiba a um imputmanager
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.cena.MouseButtonDownInput()
            if event.type == pygame.MOUSEBUTTONUP:
                self.cena.MouseButtonUpInput()
            self.cena.Input(event)
            self.guiManager.Input(event)

    def Update(self, dt):
        self.cena.Update(dt)

    def Draw(self):
        fps_text = self.font.render(f"{int(self.clock.get_fps())}", 1, (5, 120, 255))
        surfs = [self.cena.Draw(), Quadro(fps_text, fps_text.get_width(), fps_text.get_height())]
        surfs += self.guiManager.DrawGUIs()
        self.janela.Draw(surfs)

    def Run(self):
        t0 = time.time()
        while(True):
            self.Input()
            dt = time.time()-t0
            t0 = time.time()
            if dt>0.1:
                dt = 0.1
            self.Update(dt)
            self.Draw()
            self.clock.tick(self.framerate)
