import numpy as np
import pygame

from pyEngine.Cena import Cena
from pyEngine.GUI import GUIManager
from pyEngine.Quadro import Quadro

from Objetos import importNDP, importpol
from Camera3D import Camera3D
from Cameras import CameraND, ProjetorND
from Bussola3D import Bussola3D
from Controlador import ControladorOrbital

class MainCena(Cena):
    def __init__(self, largura, altura, guiManager: GUIManager=None):
        super().__init__(largura, altura, guiManager)

        #self.objs = [importpol("Objetos/kleinBottle_4.pol")]
        #self.objs = [importNDP("Objetos/hypercube.ndp")]
        #self.objs = [importNDP("Objetos/hypercube5.ndp")]
        #self.objs = [importNDP("Objetos/600_cell.ndp")]
        self.objs = [importpol("Objetos/impr_reorder.pol")]

        self.camera = Camera3D(self.largura_tela, self.altura_tela, 90, 1, [0, 0, -10])
        #self.camera4D = CameraND(4, 3, [0, 0, 0, -1])
        self.projetor = ProjetorND(6)

        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0

        self.bussola = Bussola3D(51, 51, (largura-51-10, 10), self.camera.dir)

        #self.guiManager.appendGUI(self.camera4D, ["pos", "LookAtmat"], "Camera4D")
        self.guiManager.appendGUI(self.projetor.cameras[-1], ["pos", "LookAtmat", "esfericas"], "Camera4D")
        #self.guiManager.appendGUI(self.projetor.cameras[0], ["pos", "LookAtmat"], "Camera5D")
        #self.guiManager.appendGUI(self.camera, ["pos", "vet_larg", "vet_alt", "dir"], "Camera")

        self.controlador = ControladorOrbital(self.camera, self)

        self.addUpdatable(self.controlador)
        self.addMouseButtonListener(self.controlador)

    def Input(self, event):
        #isso Deve ser resolvido com um imput manager
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass#self.controlador.InputMouseButtonDown()
        
        if event.type == pygame.MOUSEBUTTONUP:
            pass#self.controlador.InputMouseButtonUp()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.x += 0.2
            if event.key == pygame.K_a:
                self.x -= 0.2
            if event.key == pygame.K_w:
                self.y += 0.2
            if event.key == pygame.K_s:
                self.y -= 0.2
            if event.key == pygame.K_e:
                self.z += 0.2
            if event.key == pygame.K_d:
                self.z -= 0.2
            if event.key == pygame.K_r:
                self.w += 0.2
            if event.key == pygame.K_f:
                self.w -= 0.2

            if event.key == pygame.K_t:
                #print("1", self.projetor.cameras[0].esfericas)
                #print(0.1*np.pi)
                self.projetor.cameras[0].esfericas[-1] += 0.1*np.pi
                #print("2", self.projetor.cameras[0].esfericas[0])
                self.projetor.cameras[0].UpdatePos()
                #print("3", self.projetor.cameras[0].esfericas[0])

                #self.projetor.cameras[0].RotVecPos(0, 3, 0.05)
                #self.camera.RotVecPos(0, 2, np.pi*0.01)
            if event.key == pygame.K_g:
                self.projetor.cameras[0].esfericas[-1] -= 0.1*np.pi
                self.projetor.cameras[0].UpdatePos()
                #self.projetor.cameras[0].RotVecPos(0, 3, -0.05)
                #self.camera.RotVecPos(0, 2, -np.pi*0.01)
            if event.key == pygame.K_y:
                self.projetor.cameras[0].esfericas[-2] += 0.1*np.pi
                self.projetor.cameras[0].UpdatePos()

            if event.key == pygame.K_h:
                self.projetor.cameras[0].esfericas[-2] -= 0.1*np.pi
                self.projetor.cameras[0].UpdatePos()
            
            if event.key == pygame.K_u:
                self.projetor.cameras[0].esfericas[-3] += 0.1*np.pi
                self.projetor.cameras[0].UpdatePos()

            if event.key == pygame.K_j:
                self.projetor.cameras[0].esfericas[-3] -= 0.1*np.pi
                self.projetor.cameras[0].UpdatePos()
           
            if event.key == pygame.K_z:
                #self.camera.setEstiloProj(0, 3)
                self.projetor.setEstiloProj(0, 3)
            if event.key == pygame.K_x:
                #self.camera.setEstiloProj(1, 1)
                self.projetor.setEstiloProj(1, 10)


    def Update(self, dt):
        super().Update(dt)
        pos = pygame.mouse.get_pos()
        #print(self.projetor.cameras[-1].LookAtmat[-1,:-1])
        self.bussola.Update(self.camera.dir, self.projetor.cameras[-1].LookAtmat[-1,:-1])#self.camera4D.LookAtmat[-1,:-1])
        for obj in self.objs:
            #obj.RotarY(pos[0]/self.largura-0.5, dt)
            obj.Update(dt)
            #obj.MoverPara([0, 3*np.sin(3*self.z), 3*np.cos(2*self.z)])
        #self.camera4D.pos = np.array([self.x ,self.y, self.z,-1 + self.w])
        
        
        #self.projetor.cameras[-1].RotVecPos(0, 3, 0.3*dt)
        #self.projetor.cameras[0].RotVecPos(0, 4, 0.3*dt)
        
        #self.projetor.cameras[0].LookAt((0,0,0,0))
        
        self.projetor.LookAt()

        #print(self.camera4D.dir)
        #print(self.camera4D.LookAtmat)


        #vec = [np.sin((pos[0]/self.largura_tela)*-2*np.pi), np.sin((pos[1]/self.altura_tela-0.5)*np.pi), np.cos((pos[0]/self.largura_tela)*-2*np.pi)]
        #vec = [np.cos((pos[0]/self.largura_tela)*2*np.pi), np.sin((pos[1]/self.altura_tela-0.5)*np.pi), np.sin((pos[0]/self.largura_tela)*2*np.pi)]
        """
        phi = (pos[0]/self.largura_tela)*2*np.pi
        theta = (pos[1]/self.altura_tela-0.5)*np.pi
        vec = [np.cos(phi)*np.cos(theta), np.sin(theta), np.sin(phi)*np.cos(theta)]
        self.camera.pos = np.array(vec)/np.linalg.norm(vec)*10
        self.camera.LookAt((0,0,0))
        """
        #self.camera.pos[2] = self.z
        #self.z+=dt

    def Draw(self) -> Quadro:
        """#forma temporaria de lidar com loop draw
        self.janela.Draw()"""
        #Fazer camera passar a imagem diretamente para janela (Sera mesmo necessario?)
        objs3D = self.projetor.ProjetaObjs(self.objs)#self.camera4D.ProjPerspectivaObj(self.objs)
        #objs3D = self.camera4D.ProjOrtogonalObj(self.objs)
        quad = self.camera.Draw(objs3D)
        #quad = self.camera.DrawOrtogonal(objs3D)
        quad.blit(self.bussola.Draw())
        #img = pygame.Surface((10, 10))
        #img.fill((0,0,10))
        #quad.blit(Quadro(img, pos=(100, 100)))
        return quad