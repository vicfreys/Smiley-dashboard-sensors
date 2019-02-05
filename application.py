  # -*- coding: utf-8 -*-

# Modules
import pygame
import math
# Question 13
import httplib
from urlparse import urlparse
import socket

# Event constants
TIMEREVENT = pygame.USEREVENT
SENSORSEVENT = pygame.USEREVENT + 1

# Classe Sensor question 13
class Sensor:
    #Constructor
    def __init__(self, url, label, thresholds):
        self.url = url
        self.label = label
        self.thresholds = thresholds
    # Checks the url connection
    def checkUrl(self):
        self.parsedUrl = urlparse(self.url)
        self.connection = httplib.HTTPConnection(self.parsedUrl.netloc)
        try:
            self.connection.request('GET', self.url)
        except socket.gaierror:
            return False
        else:
            self.response = self.connection.getresponse()
            return self.response.status == httplib.OK
    
    # Read the url
    def read(self):
        if self.checkUrl():
            return self.response.read()
        else:
            return None
            
    # Returns the label
    def getLabel(self):
            return self.label
    
    # Question 13
    def getTransformedValue(self):
        #On lit le capteur
        x = float(self.read())
        # Si le capteur est en dehors des extremas, "y" vaut -1 ou 1 selon la borne
        if x <= self.thresholds[0]:
            y = -1
        if x >= self.thresholds[2]:
            y = 1
        # S'il est compris dans l'intervalle, "y" prend la valeur suivant la droite affine calculée
        if self.thresholds[1] < x and x < self.thresholds[2]:
            y =  (x-self.thresholds[1])/(self.thresholds[2]-self.thresholds[1]) 
        if self.thresholds[0] < x and x < self.thresholds[1]:
            y = (x-self.thresholds[0])/(self.thresholds[1]-self.thresholds[0])
            
        print(x,y)
        
        return y
    

class Emoticon:
    def __init__(self, index, sensor):
        self.size = 80
        self.border = 10
        self.textHeight = 25
        self.screen = pygame.display.get_surface()
        self.position = self.indexToPosition(index)
        # Question 9
        self.eyeWidth = 0.1* self.size
        self.eyeHeight = 0.15 * self.size
        self.eyeLeftPosition = [-0.15*self.size, 0.1*self.size]
        self.eyeRightPosition = [0.15*self.size, 0.1*self.size]
        # Question 10
        self.mouthPosition = [0, -0.25*self.size]
        self.mouthMaxHeight = 0.3*self.size
        self.mouthMaxWidth = 0.55*self.size
        self.mouthAngle = math.pi/10
        # Question 13
        self.capteur = sensor
        
        
    # Méthode permettant de calculer la largeur du cadre de l'emoticone   
    def largeurZone(self):
        return 2*self.border + self.size

    # Méthode permettant de calculer la largeur du cadre de l'emoticone
    def hauteurZone(self):
        return self.border + self.size + self.textHeight
   
   # Question 2    
    def indexToPosition(self, index):
        
        nbCaseX = self.screen.get_width()/self.largeurZone()
        i = index / nbCaseX
        j = index % nbCaseX
        
        if i< self.screen.get_height()/self.hauteurZone():
            return [j*self.largeurZone(), i*self.hauteurZone()]
        else:
            return None
    
    # Question 3
    def positionToIndex(self, position):
        
        nbCaseX = self.screen.get_width()/self.largeurZone()
   
        i = position[1] // self.hauteurZone()
        j = position[0] // self.largeurZone()
        index = j + i*nbCaseX
        return index
        
    # Question 5
    def headToArea(self, posprime):
       
        x_ecran = self.position[0] + self.border + self.size//2 + posprime[0]
        y_ecran = self.position[1] + self.border + self.size//2 - posprime[1]
        return[x_ecran, y_ecran]
    
    # Question 7
    def color(self, x):
        
        if x == 0:
            return [255, 255, 0]
        if x<0 and x>=-1:
            return [255, 255*x + 255,0]
        if x>0 and x<=1:
            return [-255*x + 255, 255, 0]
    
    # Question 8
    def head(self, x):
        
        pygame.draw.circle(self.screen, self.color(x), self.headToArea([0,0]), self.size/2)
        
    # Question 9
    def eye(self, position):
        
        pygame.draw.ellipse(self.screen, [0,0,0], [self.headToArea(position)[0]- self.eyeWidth/2, self.headToArea(position)[1] - self.eyeHeight/2, self.eyeWidth, self.eyeHeight])
     
     
    # Question 10
    def mouth(self, position, x):
         
         if x<=1 and x>=-1:
             # Si x est compris entre -0.15 et 0.15 on trace une ligne
             if x==0:
                 pygame.draw.line(self.screen, [0,0,0], [self.headToArea(position)[0]-self.mouthMaxWidth//2, self.headToArea(position)[1]], [self.headToArea(position)[0]+self.mouthMaxWidth//2, self.headToArea(position)[1]])
             if 0<x<0.15 or -0.15<x<0:
                 pygame.draw.line(self.screen, [0,0,0], [self.headToArea(position)[0]-(self.mouthMaxWidth*abs(x)/x)//2, self.headToArea(position)[1]], [self.headToArea(position)[0]+(self.mouthMaxWidth*abs(x)/x)//2, self.headToArea(position)[1]])
             # On trace le sourire
             if x>=0.15:
                pygame.draw.arc(self.screen, [0,0,0], [self.headToArea(position)[0]-self.mouthMaxWidth//2, self.headToArea(position)[1]-self.mouthMaxHeight//2-(self.mouthMaxWidth//2)*math.tan(self.mouthAngle), self.mouthMaxWidth, self.mouthMaxHeight], math.pi+self.mouthAngle, 2*math.pi-self.mouthAngle)
             # On trace la grimace
             if x<=-0.15:
                 pygame.draw.arc(self.screen, [0,0,0], [self.headToArea(position)[0]-self.mouthMaxWidth//2, self.headToArea(position)[1]-self.mouthMaxHeight//2+(self.mouthMaxWidth//2)*math.tan(self.mouthAngle), self.mouthMaxWidth, self.mouthMaxHeight], self.mouthAngle, math.pi-self.mouthAngle)
         else:
             return None
    
    # Question 11
    def drawEmoticon(self,x):
        # On ajoute les différentes méthodes afin de reproduire l'ensemble de l'emoticone
        self.head(x)
        self.eye(self.eyeLeftPosition)
        self.eye(self.eyeRightPosition)
        self.mouth(self.mouthPosition, x)
    
    # Question 12
    def drawLabels(self, labels):
        
        font = pygame.font.Font(None, 14)
        textimage1 = font.render(labels[0], 1, [255,255,255]) 
        
        # La coordonnée du point d'origine se trouve à une demi-largeur de la zone du texte afin que le cadre soit centré
        x = -textimage1.get_width()//2
        y = -self.size//2
        
        self.screen.blit(textimage1, self.headToArea([x, y]))
        
        textimage2 = font.render(labels[1],1,[255,255,255])
        
        x1 = -textimage2.get_width()//2
        # On ajoute la hauteur du premier cadre afin de l'avoir en dessous sans chevauchement
        y1 = -self.size//2-textimage1.get_height()
        
        self.screen.blit(textimage2, self.headToArea([x1, y1]))

    # Question 13
    def draw(self):
        # On dessine un rectangle noir afin de supprimer l'ancienne image
        pygame.draw.rect(self.screen,[0,0,0,], [self.position[0], self.position[1], self.size+2*self.border, self.size+self.border+self.textHeight],0)
        # Le parametre x est remplacé par la méthode getTransformedValue()
        self.drawEmoticon(self.capteur.getTransformedValue())
        self.drawLabels([self.capteur.getLabel(), self.capteur.read()])
    
    # Question 15    
    def inArea(self, coordsouris):
        # On repère l'index du clique de la souris
        indexsouris = self.positionToIndex(coordsouris)
        # Si la position du clique de la souris correspond à la position d'une zone emoticone, on retourne vrai
        if self.indexToPosition(indexsouris) == self.position:
            return True
        else:
            return False
    
    # Question 15        
    def setSelected(self):
            self.selected = True
    
    # Question 15
    def resetSelected(self):
            self.selected = False
    
    # Question 15
    def isSelected(self):
        return self.selected
    
    # Question 15
    def move(self, coordsouris):
        # On affiche un rectangle noir aux dimensions des cases d'emoticone
        pygame.draw.rect(self.screen,[0,0,0,], [self.position[0], self.position[1], self.size+2*self.border, self.size+self.border+self.textHeight],0)
        # On repère l'index du clique de la souris par sa position
        index = self.positionToIndex(coordsouris)
        # L'emoticone prend la prend la place de la zone
        self.position = self.indexToPosition(index)
        # On dessine l'emoticone
        self.draw()    
        
# Defines the main function
def main():

    #Initializes pygame
    pygame.init()

    # Sets the screen size.
    pygame.display.set_mode((800, 600))

    # Sets the timer to check event every 100 ms
    pygame.time.set_timer(TIMEREVENT, 100)

    # Sets the timer to read the sensors every 1000 ms
    pygame.time.set_timer(SENSORSEVENT, 1000)

    # On crée la liste de capteurs
    sensors =  []
    sensors.append(Sensor('http://www.polytech.univ-savoie.fr/apps/myreader/capteur.php?capteur=epua_b204_clim','Temp.Clim B204',[22, 24, 27]))
    sensors.append(Sensor('http://www.polytech.univ-savoie.fr/apps/myreader/capteur.php?capteur=epua_b204_coursive','Temp.Cours B204',[18.5,27,30]))
    sensors.append(Sensor('http://www.polytech.univ-savoie.fr/apps/myreader/capteur.php?capteur=epua_b204_centre','Temp.Cent B204',[22, 24,28]))
    sensors.append(Sensor('http://www.polytech.univ-savoie.fr/apps/myreader/capteur.php?capteur=epua_toiture','Temp.Toit',[5,35,40]))
    sensors.append(Sensor('http://www.polytech.univ-savoie.fr/apps/myreader/capteur.php?capteur=epua_onduleur1_watts','Puis.Ond.',[8000,8100,10000]))
    
    # On crée la liste d'emoticones    
    emoticons = []
    
    # On remplit la liste grâce à une boucle pour, afin d'ajouter autant d'emoticone qu'il y a de capteurs
    for i in range(len(sensors)):
        emoticons.append(Emoticon(i,sensors[i]))

    # Infinite loop
    while True:

        # Waits for an event
        event = pygame.event.wait()

        # Reads information from the sensors.
        if event.type == SENSORSEVENT:
            for i in range(len(sensors)):
                emoticons[i].draw()

        # Draws what was written to the screen based on the timer
        elif event.type == TIMEREVENT:
            pygame.display.flip()

        # Checks if the quit event is set
        elif event.type == pygame.QUIT:
            # Quits
            pygame.quit()
            break
        
        # Question 15
        # On parcours les émoticônes
        for i in range(len(emoticons)):
            
            # Si l'on détecte un clic de la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                # On initialise l'état de l'émoticône 
                emoticons[i].resetSelected()
                # Si l'on clique dans une zone de l'emoticone
                if emoticons[i].inArea(event.pos):
                    # On passe l'état de l'emoticône à sélectionner
                    emoticons[i].setSelected()
            # Si l'on détecte un relâchement du clic de la souris        
            if event.type == pygame.MOUSEBUTTONUP:
                
                # Si un emoticône est sélectionnée
                if emoticons[i].isSelected():
                    # On parcours l'ensemble est émoticônes afin de savoir si l'on relâche sur une zone d'emoticone
                    for emoticon in emoticons:
                        if emoticon.inArea(event.pos):
                            # On déselectionne l'emoticone afin de ne pas le déplacer sur cet emplacement déjà occupé
                            emoticons[i].resetSelected()
                    # Si l'émoticône est dans une zone libre on le déplace et on passe son état à déselectionner
                    if emoticons[i].isSelected():
                        emoticons[i].move(event.pos)
                        emoticons[i].resetSelected()

               
                        
# Calls the main function
if __name__ == "__main__":
    main()
