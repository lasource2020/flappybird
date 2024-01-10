from turtle import window_height
import pygame
import numpy
import random
pygame.init()

#On charge les propriétés de la window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock() 

#On charge les textures et on déclare leur propriétés
backgroundSprite = pygame.image.load('Textures/background.png')
background1PosX = 0
background2PosX = background1PosX + WINDOW_WIDTH;
#On charge les textures du player et on déclare ses propriétés
playerSprite = pygame.image.load('Textures/birdSprite.png')
playerSprite = pygame.transform.scale(playerSprite, (50, 25))
IsFlapping = False
playerSpritePosX = WINDOW_WIDTH / 2
playerSpritePosY = WINDOW_HEIGHT / 2
flapAmplitude = 50
flapSpeed = 1
fallSpeed = 1
lastPlayerPosY = 0
#On charge la texture du tuyau et déclare les propriétés du tuyau dans une classe
pipeSpriteUp = pygame.image.load('Textures/pipe.png')
pipeSpriteDown = pygame.image.load('Textures/pipe.png')
pipeSpeed = 3
pipeArray = []

#Inputs related
isSpacePressed = False
isFirstPress = True
gameStarted = False


def lerp(start, end, t):
    return start + t * (end - start)

class Pipe:
    def __init__(self):
        self._pipeSpriteUp  = pipeSpriteUp
        self._pipeSpriteDown = pipeSpriteDown
        self.upX = WINDOW_WIDTH
        self.upY = random.randint(int((pipeSpriteUp.get_height()/2)* -1), int(WINDOW_HEIGHT - pipeSpriteUp.get_height() - 100))
        self.downX = WINDOW_WIDTH
        self.downY = self.upY + pipeSpriteUp.get_height() + 100
        print(random.randint(50, int(WINDOW_HEIGHT/2-100)))
        pipeArray.append(self)
    def DrawPipe(self):
        window.blit(self._pipeSpriteUp, (self.upX, self.upY))
        window.blit(self._pipeSpriteDown, (self.downX, self.downY))
    def MovePipe(self):
        self.upX -= pipeSpeed
        self.downX -= pipeSpeed
        if(self.upX < WINDOW_WIDTH/3):
            Pipe()
            del pipeArray[0]

def MoveBackground():
    global background1PosX
    global background2PosX
    
    background1PosX -= 1
    background2PosX -= 1

    if background1PosX + backgroundSprite.get_width() < 0:
        background1PosX = background2PosX + backgroundSprite.get_width()
    elif background2PosX + backgroundSprite.get_width() < 0:
        background2PosX = background1PosX + backgroundSprite.get_width()

def DrawSprites():
    window.fill((0, 0, 0))
    
    window.blit(backgroundSprite, (background1PosX, 0))
    window.blit(backgroundSprite, (background2PosX, 0))
    window.blit(playerSprite, (playerSpritePosX, playerSpritePosY))
    for pipe in pipeArray:
        pipe.DrawPipe()
    pygame.display.update()

def BirdFall():
    global playerSpritePosY
    global lastPlayerPosY
    global fallSpeed

    if(IsFlapping == False):
        playerSpritePosY += fallSpeed
        fallSpeed = lerp(20, 1, lastPlayerPosY/playerSpritePosY)

    else:
        fallSpeed = 1

def BirdFlap():
    global playerSpritePosY   
    global lastPlayerPosY
    global IsFlapping
    global flapSpeed
    
    goal = lastPlayerPosY - flapAmplitude    

    if IsFlapping:
        flapSpeed = lerp(25, 1, goal/playerSpritePosY)
        playerSpritePosY -= flapSpeed
        
    if playerSpritePosY < goal:
        IsFlapping = False
        lastPlayerPosY = playerSpritePosY

def CheckInputs():
    global isSpacePressed
    global IsFlapping
    global lastPlayerPosY
    global gameStarted
    global isFirstPress

    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE] and isSpacePressed == False:
        lastPlayerPosY = playerSpritePosY
        IsFlapping = True
        isSpacePressed = True
        if isFirstPress:
            gameStarted = True
            isFirstPress = False
            Pipe()

    elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE and isSpacePressed:
        isSpacePressed = False
      
def CheckCollision():
    global WINDOW_HEIGHT
    global playerSpritePosY
    global playerSprite
    global gameStarted
    global isFirstPress

    if(playerSpritePosY <= 1 or playerSpritePosY >= WINDOW_HEIGHT - playerSprite.get_height()):
        gameStarted = False
        isFirstPress = True
        
        
#GameLoop
isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            
    clock.tick(45);
    
    CheckInputs()
    if(gameStarted):
        CheckCollision()
        MoveBackground()
        BirdFall()
        BirdFlap()
        for pipe in pipeArray:
            pipe.MovePipe()
    DrawSprites()
    
pygame.quit()
