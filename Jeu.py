#!/usr/bin/python

import pygame
import LabIA
import time

pygame.init()

WIDTH = 800
HEIGHT = 600
BLUE = (0,0,255)
BLACK = (0,0,0)

x = 100
y = 100

surface = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Labs")

def brick(x,y, img):
   surface.blit(img,(x,y)) 

def message(txt,size,color):
    text = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size).render(txt, True, color)
    textRect = text.get_rect()
    textRect.center = WIDTH/2, ((HEIGHT/2)-50)
    textRect.center = WIDTH/2, 50
    surface.blit(text, textRect)

def load(fileName):
    f=open(fileName,"r")
    labi=[]
    d=f.read(1)
    donotreadnext=False
    line=[]
    while d != '':
        if d == "\n":
            labi.append(line)
            line=[]
        else:
            if d == "-":
                donotreadnext=True
                line.append("*")
            elif donotreadnext == False:
                line.append(d)
            else:
                donotreadnext=False
        d=f.read(1)
    f.close()
    return labi

def printLabi(labi):
    posx=100
    posy=100
    b_height = 30
    b_width = 31
    for line in labi:
        posx=100-b_width
        for char in line:
            posx += b_width
            if str(char) == "1":
                brick(posx,posy,img)
        posy += b_height

def path(x,y,img):
    brick((100-31)+((x+1)*31),(100)+(y*30),img)

img = pygame.image.load("Brick.png")
imgMagie = pygame.image.load("Magie.png")
print("Loading Labi")
labi = load("./minilabi")
print("Labi Loaded")
for line in labi:
    print(line)

p=LabIA.Position(1,1)
maze=LabIA.Maze(labi,p)
ia = LabIA.IAHistPathFinder(p,maze)


end = False
surface.fill(BLUE)
printLabi(labi)
pygame.display.update()
try:
    pos=[]
    pos=ia.walkTo(maze.sortie)
    index=0
    revpos=pos[::-1]
    for elt in range(0,len(pos),3):
        try:
            print(revpos[elt],revpos[elt+1],revpos[elt+2])
        except:
            try:
                print(revpos[elt],revpos[elt+2])
            except:
                print(revpos[elt])

    path(1,1,imgMagie)
    pygame.display.update()
    for imagepos in pos[::-1]:
        time.sleep(0.2)
        path(imagepos.x,imagepos.y,imgMagie)
        pygame.display.update()
except LabIA.CantMoveException as e:
    if maze.sortie == ia.historyOfPos.currentNode.position:
        print("Vous etes arrives !!!")
    else:
        print(e)
except LabIA.MazeNoWayOutException as e2:
    message(e2.message,24,(255,0,0))
    pygame.display.update()
    print(e2)
except Exception as ex:
    print(ex)
    pygame.quit()
    quit()

while not end:
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
            end = True



pygame.quit()
quit()


    
