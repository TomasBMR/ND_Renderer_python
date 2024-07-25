import pygame
import numpy as np

from .Quadro import Quadro

class GUIManager:
    def __init__(self):
        self.GUIs: list[GUI] = []

        self.offSet = 10

        self.altura:int = self.offSet

    def Input(self, event):
        for gui in self.GUIs:
            gui.Input(event)

    def appendGUI(self, objeto, atributos: list[str], nome: str):
        novoGUI = GUI(objeto, atributos, nome, (10, self.altura))
        surf, _ = novoGUI.getInterface().getSurfnPos()
        self.altura += self.offSet + surf.get_height()
        self.GUIs.append(novoGUI)
    
    def DrawGUIs(self) -> list[Quadro]:
        return [gui.getInterface() for gui in self.GUIs]


class GUI:
    """Recebe atributos de uma classe os escreve em uma imagem
    para facilitar a implementacao da coisas"""
    def __init__(self, objeto, atributos:list[str], nome: str, pos:tuple[int, int]=(10,10)):
        self.objeto = objeto
        self.listaAtributos = atributos

        self.attrs = self.getAttrs()

        self.nome = nome
        self.pos = pos
        self.largura = 200
        self.altura = 300

        self.corFundo = (22, 34, 56)
        self.corFont = (108, 110, 143)
        self.font1 = pygame.font.SysFont("Arial", 18)
        self.font2 = pygame.font.SysFont("Arial", 15)

        self.calcProps()

        self.quadro = Quadro(pygame.Surface((self.largura, self.altura)), pos=pos)

    def Input(self, event):
        pass


    def getAttrs(self):
        return [(chave, str(self._round(valor))) for chave, valor in self.objeto.__dict__.items() if chave in self.listaAtributos]

    def _round(self, val):
        if isinstance(val, float):
            return round(val, 3)
        elif isinstance(val, np.ndarray):
            return np.around(val, 3)
        return val


    def getInterface(self) -> Quadro:
        interface = pygame.Surface((self.largura, self.altura))

        nome = self.font1.render(f"{self.nome}", 1, self.corFont)
        interface.blit(nome, (2,2))

        ypos = nome.get_height()

        self.attrs = self.getAttrs()
        for i, (chave, valor) in enumerate(self.attrs):
            txt = f"{chave}: \n{valor}"
            lins = txt.split("\n")
            #lins = [len(lins[0])*" "+lin  if i != 0 else lins[0] for i, lin in enumerate(lins)]
            for lin in lins:
                txtAttr = self.font2.render(lin, 0, self.corFont)
                interface.blit(txtAttr, (4, ypos))
                ypos += txtAttr.get_height()
        self.calcProps()
        self.quadro.setSurf(interface)
        return self.quadro
    
    def calcProps(self):
        """Encontra a melhor altura e largura para o display dos atributos"""
        #Altura do nome
        nome = self.font1.render(f"{self.nome}", 1, self.corFont)

        linsW = [nome.get_width()]
        linsH = [nome.get_height()]
        self.attrs = self.getAttrs()
        for (chave, valor) in self.attrs:
            linsRender = [self.font2.render(lin, 0, self.corFont) for lin in f"{chave}: \n{valor}".split("\n")]
            linsW += [lin.get_width() for lin in linsRender]
            linsH += [lin.get_height() for lin in linsRender]

        self.largura = max(linsW) + 10
        self.altura = sum(linsH) + 10


if __name__ == "__main__":
    pygame.init()
    class classeTeste:
        def __init__(self, a):
            self.atr1 = a
            self.atr2 = 23
            self.atr3 = [1, 2, 3]
        
        def metodo1(self):
            for i in self.atr3:
                print(i, self.atr2)

    t = classeTeste(1)

    gui = GUI(t, ["atr1", "atr2"])

    gui.printAttrs()