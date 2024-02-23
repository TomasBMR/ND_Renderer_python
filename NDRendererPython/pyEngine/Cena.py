from abc import ABC, abstractmethod
from .GUI import GUIManager
from .Quadro import Quadro

class Cena(ABC):
    def __init__(self, largura, altura, guiManager: GUIManager=None):
        #Algumas coisas não deveriam pertencer a cena (por isso virou um classe pai!!)
        self.inputManager = None
        self.guiManager: GUIManager = guiManager

        self.largura_tela = largura
        self.altura_tela = altura

    def Input(self, event):
        #Inputs de objetos na cena são chamados aqui
        pass

    def Update(self, dt):
        #Estado dos objetos na cena são chamados aqui
        pass
    
    @abstractmethod
    def Draw(self) -> Quadro:
        #Retorna uma superficie que se deseja desenhar na tela
        pass
        """#forma temporaria de lidar com loop draw
        self.janela.Draw()"""
        #Fazer camera passar a imagem diretamente para janela
