from abc import ABC, abstractmethod
from .GUI import GUIManager
from .Quadro import Quadro

class Cena(ABC):
    def __init__(self, largura, altura, guiManager: GUIManager=None):
        #Algumas coisas não deveriam pertencer a cena (por isso virou um classe pai!!)
        self.inputManager = None
        self.guiManager: GUIManager = guiManager

        #Isso provavelmente nao deveria ficar aqui...
        self.largura_tela = largura
        self.altura_tela = altura

        self.updatableObj = []

        self.mouseButtonListeners = []


    def Input(self, event):
        #Inputs de objetos na cena são chamados aqui
        pass
    
    ##Isso vai para um input manager
    def addMouseButtonListener(self, obj:object):
        self.mouseButtonListeners.append(obj)

    def MouseButtonDownInput(self):
        for listener in self.mouseButtonListeners:
            listener.InputMouseButtonDown()
    
    def MouseButtonUpInput(self):
        for listener in self.mouseButtonListeners:
            listener.InputMouseButtonUp()
    
    def addUpdatable(self, obj:object):
        self.updatableObj.append(obj)

    def Update(self, dt):
        for updatable in self.updatableObj:
            updatable.Update(dt)
        #Fazer lista de objetos updataveis e chamar por aqui

    def getProporcoes(self):
        return self.largura_tela, self.altura_tela

    #def InnerUpdate(self, dt):
        #Estado dos objetos na cena são chamados aqui
    #    for updatable in self.updatableObj:
    #        updatable.Update(dt)
        
    #    self.Update(dt)

    
    @abstractmethod
    def Draw(self) -> Quadro:
        #Retorna uma superficie que se deseja desenhar na tela
        pass
        """#forma temporaria de lidar com loop draw
        self.janela.Draw()"""
        #Fazer camera passar a imagem diretamente para janela
