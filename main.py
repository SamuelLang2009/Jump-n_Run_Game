import pygame
pygame.init()
import PySimpleGUI as sg
from plyer import notification
import os

SCREEN_X=1600
SCREEN_Y=800

Y_VELOCITY = 15
JUMP_HEIGHT= 15
Y_GRAVITY = 0.8

# genutzte Farbe
ORANGE  = ( 255, 140, 0)
ROT     = ( 255, 0, 0)
GRUEN   = ( 0, 255, 0)
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)

BG=pygame.transform.scale2x(pygame.image.load(os.path.join("background.png")))
PLAYER_IMG=pygame.image.load(os.path.join("player.png"))
KEY=pygame.transform.scale(pygame.image.load(os.path.join("key.png")),(80,80))
PLAYER_IMG_SMALL=pygame.transform.scale(pygame.image.load(os.path.join("player.png")),(33,33))
KEY_SMALL=pygame.transform.scale(pygame.image.load(os.path.join("key.png")),(40,40))
SWITCH_RECHTS=pygame.transform.scale(pygame.image.load(os.path.join("RECHTS.png")),(60,60))
SWITCH_RECHTS_SMALL=pygame.transform.scale(pygame.image.load(os.path.join("RECHTS.png")),(30,30))
SWITCH_UP=pygame.transform.scale(pygame.image.load(os.path.join("UP.png")),(60,60))
SWITCH_UP_SMALL=pygame.transform.scale(pygame.image.load(os.path.join("UP.png")),(30,30))
SWITCH_DOWN=pygame.transform.scale(pygame.image.load(os.path.join("DOWN.png")),(60,60))
SWITCH_DOWN_SMALL=pygame.transform.scale(pygame.image.load(os.path.join("DOWN.png")),(30,30))
SWITCH_KLEIN=pygame.transform.scale(pygame.image.load(os.path.join("KLEINER.png")),(60,60))
SWITCH_GROSS=pygame.transform.scale(pygame.image.load(os.path.join("GRÖSSER.png")),(30,30))





class player:
    def __init__(self,x,y,a,movementspeed) -> None:
        self.x=x
        self.y=y
        self.size=a
        self.movementspeed=movementspeed
        self.topleft=[self.x,self.y]
        self.topright=[self.x+self.size,self.y]
        self.bottomleft=[self.x,self.y+self.size]
        self.bottomright=[self.x+self.size,self.y+self.size]
        self.velocity=15
        self.direction=1
    
    def actualise(self):
        self.topleft=[self.x,self.y]
        self.topright=[self.x+self.size,self.y]
        self.bottomleft=[self.x,self.y+self.size]
        self.bottomright=[self.x+self.size,self.y+self.size]
    
    def move(self,mover):
        if mover>1:
            self.x=mover
        else:
            if self.size==33:
                self.x+=(mover*self.movementspeed)/2
            else:
                self.x+=(mover*self.movementspeed)

    
    def paint(self):
        if self.direction==1:
            #pygame.draw.rect(screen,WEISS,[self.x,self.y,self.size,self.size])
            if self.size==100:
                screen.blit(PLAYER_IMG,(self.x,self.y))
            else:
                screen.blit(PLAYER_IMG_SMALL,(self.x,self.y))
        elif self.direction==2:
            if self.size==100:
                screen.blit(PLAYER_IMG,(self.y,self.x))
            else:
                screen.blit(PLAYER_IMG_SMALL,(self.y,self.x))
        elif self.direction==3:
            if self.size==100:
                screen.blit(PLAYER_IMG,(self.x,self.y))
            else:
                screen.blit(PLAYER_IMG_SMALL,(self.x,self.y))
        
    def jump(self,ground,difficultie):
        if self.size!=33:
            difs=[0.58,0.68,0.73]
        else:
            difs=[0.58*2,0.68*2,0.73*2]
        if isgroundSuper(self.x,self.y,self.size,currentscene,keys):
            difs=[0.58/3,0.68/3,0.73/3]
        if self.direction!=3:
            self.y -= self.velocity
            self.velocity -= difs[difficultie]
            if self.y>ground-self.size:
                self.velocity = 15
                self.y=ground-self.size
                return 1
            return 0
        else:
            self.y += self.velocity
            self.velocity -= difs[difficultie]
            if self.y<ground:
                self.velocity = 15
                self.y=ground
                return 1
            return 0
        
    def ResetJump(self):
        self.velocity=15

    def fall(self,ground):
        if self.direction!=3:
            if self.y+15+self.size<=ground:
                self.y += 15
            else:
                self.y=ground-self.size
        else:
        
            if self.y-15>=ground:
                self.y -= 15
            else:
                self.y=ground

        
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def geta(self):
        return self.size
    
    def SceneUp(self):
        if self.direction!=2:
            self.x=0
        else:
            self.y=self.x
            self.x=0
            self.direction=1
    def SceneDown(self):
        self.x=1600-self.size
        
    def SetX(self,x):
        self.x=x
        
    def SetY(self,x):
        self.y=x
        
    def changeDirection(self,direction):
        if direction ==2:
            speicher=self.x
            self.x=self.y
            self.y=speicher
            self.direction=2
        if direction==3:
            self.direction=3
        if self.direction==3 and direction==1:
            self.direction=1
        if self.direction==2 and direction==1:
            self.direction=1
            speicher=self.x
            self.x=self.y
            self.y=speicher

    def getsmall(self):
        self.size=33
    def getbig(self):
        self.x-=67
        self.y-=67
        self.size=100
            

class construct:
    def __init__(self,scene,x,y,width,height,color) -> None:
        self.scene=scene
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.topleft=[self.x,self.y]
        self.topright=[self.x+self.width,self.y]
        self.bottomleft=[self.x,self.y+self.height]
        self.bottomright=[self.x+self.width,self.y+self.height]
        self.direction=1
        if self.height>self.width:
            self.l=pygame.transform.rotate(pygame.image.load(os.path.join("Plattform.png")),90)
        else:
            self.l=pygame.image.load(os.path.join("Plattform.png"))
        self.image=pygame.transform.scale(self.l,(self.width,self.height))
        
    
    def ground(self, x, y, size, scene):
        if self.direction!=3:
            if self.scene == scene:
                if x < self.x + self.width: 
                    if x + size >= self.x:
                        if y + size <= self.y:
                            return self.y
            return float("inf")
        else:
            if self.scene == scene:
                if x < self.x + self.width: 
                    if x + size >= self.x:
                        if y  >= self.y:
                            return self.y+self.height
            return -100
    
    def paint(self,scene):
        if self.scene==scene:
            if self.direction==1 or self.direction==3 or self.direction==5 or self.direction==6:
                #pygame.draw.rect(screen,self.color,[self.x,self.y,self.width,self.height])
                screen.blit(self.image,(self.x,self.y))
            elif self.direction==2:
                #pygame.draw.rect(screen,self.color,[self.y,self.x,self.height,self.width])
                screen.blit(self.image,(self.y,self.x))

    def getScene(self):
        return self.scene
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getwidth(self):
        return self.width
    def getheight(self):
        return self.height
    
    def changeDirection(self,direction):
        if direction==2 and self.scene==currentscene:
            speicher=self.x
            self.x=self.y
            self.y=speicher
            speicher=self.height
            self.height=self.width
            self.width=speicher
            
        if direction==3:
            self.direction=3
        if self.direction==3 and direction==1:
            self.direction=1
        if self.direction==2 and direction==1 and self.scene==10:
            self.direction=1
            speicher=self.x
            self.x=self.y
            self.y=speicher
            speicher=self.height
            self.height=self.width
            self.width=speicher
        self.direction=direction
        
    
class moverp:
    def __init__(self,scene,x,y,width,height,color,end,speed) -> None:
        self.scene=scene
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.topleft=[self.x,self.y]
        self.topright=[self.x+self.width,self.y]
        self.bottomleft=[self.x,self.y+self.height]
        self.bottomright=[self.x+self.width,self.y+self.height]
        self.direction=1
        self.start=x
        self.end=end
        self.speed=speed
        self.check=0
        if end<x:
            self.start=end
            self.end=x
    
    def ground(self, x, y, size, scene):
        if self.direction!=3:
            if self.scene == scene:
                if x < self.x + self.width: 
                    if x + size >= self.x:
                        if y + size <= self.y:
                            return self.y
            return float("inf")
        else:
            if self.scene == scene:
                if x < self.x + self.width: 
                    if x + size >= self.x:
                        if y  >= self.y:
                            return self.y+self.height
            return -100
    
    def paint(self,scene):
        if self.scene==scene:
            
            pygame.draw.rect(screen,self.color,[self.x,self.y,self.width,self.height])
            

    def getScene(self):
        return self.scene
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getwidth(self):
        return self.width
    def getheight(self):
        return self.height
    
    def changeDirection(self,direction):
        self.direction=direction
        if direction==2 and self.scene==currentscene:
            pass
        if direction==3:
            self.direction=3
        if self.direction==3 and direction==1:
            self.direction=1
    
    def tick(self):
        if self.x>=self.end:
            self.check=1
        if self.x<=self.start:
            self.check=0
        if self.check:
            self.x-=self.speed
        else:
            self.x+=self.speed
    

class hider:
    def __init__(self,scene,x,y,width,height,color,q,w,direction=1) -> None:
        self.scene=scene
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.topleft=[self.x,self.y]
        self.topright=[self.x+self.width,self.y]
        self.bottomleft=[self.x,self.y+self.height]
        self.bottomright=[self.x+self.width,self.y+self.height]
        self.direction=direction
        self.period=q
        self.ticker=w
        self.visible=1
    
    def ground(self, x, y, size, scene):
        if self.direction!=3:
            if self.scene == scene:
                if x < self.x + self.width: 
                    if x + size >= self.x:
                        if y + size <= self.y:
                            if self.visible:
                                return self.y
            return float("inf")
        else:
            if self.scene == scene:
                if x < self.x + self.width: 
                    if x + size >= self.x:
                        if y  >= self.y:
                            if self.visible:
                                return self.y+self.height
            return -100
    
    def paint(self,scene):
        if self.visible:
            if self.scene==scene:
                if self.direction==1 or self.direction==3 or self.direction==5 or self.direction==6:
                    pygame.draw.rect(screen,self.color,[self.x,self.y,self.width,self.height])
                elif self.direction==2:
                    pygame.draw.rect(screen,self.color,[self.y,self.x,self.height,self.width])

    def getScene(self):
        return self.scene
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getwidth(self):
        return self.width
    def getheight(self):
        return self.height
    
    def changeDirection(self,direction):
        self.direction=direction
        if direction==2 and self.scene==currentscene:
            speicher=self.x
            self.x=self.y
            self.y=speicher
            speicher=self.height
            self.height=self.width
            self.width=speicher
        if direction==3:
            self.direction=3
        if self.direction==3 and direction==1:
            self.direction=1
    
    def ttick(self):
        self.ticker+=1
        if self.ticker==self.period:
            self.ticker=0
            if self.visible:
                self.visible=0
            else:
                self.visible=1


class jumper:
    def __init__(self,scene,x,y,width,height,color) -> None:
        self.scene=scene
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.topleft=[self.x,self.y]
        self.topright=[self.x+self.width,self.y]
        self.bottomleft=[self.x,self.y+self.height]
        self.bottomright=[self.x+self.width,self.y+self.height]
        self.direction=1
        if self.height>self.width:
            self.l=pygame.transform.rotate(pygame.image.load(os.path.join("JUMPER.png")),90)
        else:
            self.l=pygame.image.load(os.path.join("JUMPER.png"))
        self.image=pygame.transform.scale(self.l,(self.width,self.height))
    
    def ground(self, x, y, size, scene):
        if self.direction!=3:
            if self.scene == scene:
                if x < self.x + self.width: 
                    if x + size >= self.x:
                        if y + size <= self.y:
                            return self.y
            return float("inf")
        else:
            if self.scene == scene:
                if x < self.x + self.width: 
                    if x + size >= self.x:
                        if y  >= self.y:
                            return self.y+self.height
            return -100
    
    def paint(self,scene):
        if self.scene==scene:
            if self.direction==1 or self.direction==3 or self.direction==5 or self.direction==6:
                #pygame.draw.rect(screen,self.color,[self.x,self.y,self.width,self.height])
                screen.blit(self.image,(self.x,self.y))
            elif self.direction==2:
                #pygame.draw.rect(screen,self.color,[self.y,self.x,self.height,self.width])
                screen.blit(self.image,(self.y,self.x))

    def getScene(self):
        return self.scene
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getwidth(self):
        return self.width
    def getheight(self):
        return self.height
    
    def changeDirection(self,direction):
        if direction==2 and self.scene==currentscene:
            speicher=self.x
            self.x=self.y
            self.y=speicher
            speicher=self.height
            self.height=self.width
            self.width=speicher
            
        if direction==3:
            self.direction=3
        if self.direction==3 and direction==1:
            self.direction=1
        if self.direction==2 and direction==1:
            self.direction=1
            speicher=self.x
            self.x=self.y
            self.y=speicher
            speicher=self.height
            self.height=self.width
            self.width=speicher
        self.direction=direction
        
        
    
class key:
    def __init__(self,scene,x,y,size) -> None:
        self.scene=scene
        self.x=x
        self.y=y
        self.size=size
        self.touched=0
    
    def paint(self,scene):
        if scene==self.scene:
            if not self.touched:
                #pygame.draw.circle(screen, ORANGE,[self.x,self.y],self.size)
                if self.size==30:
                    screen.blit(KEY,(self.x-self.size,self.y-self.size))
                else:
                    screen.blit(KEY_SMALL,(self.x-self.size,self.y-self.size))
             
    def prooftouch(self,playerx,playery,playera,scene):
        if scene==self.scene:
            if direction!=2:
                if self.x-playera-self.size<playerx<self.x+self.size and self.y-playera-self.size<playery<self.y+self.size:
                    self.touched=1
            else:
                if self.x-playera-self.size<playery<self.x+self.size and self.y-playera-self.size<playerx<self.y+self.size:
                    self.touched=1
                
    def isTouched(self):
        return self.touched
    
class switch:
    def __init__(self,scene,x,y,size,direction) -> None:
        self.scene=scene
        self.x=x
        self.y=y
        self.size=size
        self.touched=0
        self.checked=0
        self.d=direction

    def paint(self,scene):
        if scene==self.scene:
            if not self.touched:
                if self.d==2:
                    #pygame.draw.circle(screen, GRUEN,[self.x,self.y],self.size)
                    if self.size==40:
                        screen.blit(SWITCH_RECHTS,(self.x-self.size,self.y-self.size))
                    else:
                        screen.blit(SWITCH_RECHTS_SMALL,(self.x-self.size,self.y-self.size))
                if self.d==3:
                    #pygame.draw.circle(screen, GRUEN,[self.x,self.y],self.size)
                    if self.size==40:
                        screen.blit(SWITCH_UP,(self.x-self.size,self.y-self.size))
                    else:
                        screen.blit(SWITCH_UP_SMALL,(self.x-self.size,self.y-self.size))
                if self.d==1:
                    #pygame.draw.circle(screen, GRUEN,[self.x,self.y],self.size)
                    if self.size==40:
                        screen.blit(SWITCH_DOWN,(self.x-self.size,self.y-self.size))
                    else:
                        screen.blit(SWITCH_DOWN_SMALL,(self.x-self.size,self.y-self.size))
                if self.d==5:
                    screen.blit(SWITCH_GROSS,(self.x-self.size,self.y-self.size))
                if self.d==6:
                    screen.blit(SWITCH_KLEIN,(self.x-self.size,self.y-self.size))
                
             
    def prooftouch(self,playerx,playery,playera,scene):
        if scene==self.scene:
            if self.x-playera-self.size<playerx<self.x+self.size and self.y-playera-self.size<playery<self.y+self.size:
                self.touched=1
                
    def isTouched(self,direction):
        if self.checked==0 and self.touched:
            self.checked=1
            return self.d
        return direction

            

def getGround(playerx,playery,a,currentscene,keys):

    if direction!=3:
        ground = float('inf')

        if not keys[currentscene-1].isTouched():
            ground=1600
        prevground=0
        for c in constructs[currentscene-1]:
            ground = min(ground, c.ground(playerx, playery, a, currentscene))
        prevground=ground
        for j in jumpers:
            ground = min(ground, j.ground(playerx, playery, a, currentscene))
        for h in hiders:
            ground = min(ground, h.ground(playerx, playery, a, currentscene))
        for m in movers:
            ground = min(ground, m.ground(playerx, playery, a, currentscene))
        
        return ground
    else:
        ground = -100
        for c in constructs[currentscene-1]:
            ground = max(ground, c.ground(playerx, playery, a, currentscene))
        for h in hiders:
            ground = max(ground, h.ground(playerx, playery, a, currentscene))
        for m in movers:
            ground = max(ground, m.ground(playerx, playery, a, currentscene))
        return ground

def isgroundSuper(playerx,playery,a,currentscene,keys):

    if direction!=3:
        ground = float('inf')

        if not keys[currentscene-1].isTouched():
            ground=1600
        prevground=0
        for c in constructs[currentscene-1]:
            ground = min(ground, c.ground(playerx, playery, a, currentscene))
        for h in hiders:
            ground = min(ground, h.ground(playerx, playery, a, currentscene))
        for m in movers:
            ground = min(ground, m.ground(playerx, playery, a, currentscene))
        prevground=ground
        for j in jumpers:
            ground = min(ground, j.ground(playerx, playery, a, currentscene))
        if prevground!=ground:
            return 1
        
        return 0
    else:
        ground = -100
        for c in constructs[currentscene-1]:
            ground = max(ground, c.ground(playerx, playery, a, currentscene))
        return 0


def changeMover(mover):
    if mover!=0:
        for c in constructs[currentscene-1]:
            if c.getScene()==currentscene:
                if p1.gety()+p1.geta()>c.gety() and p1.gety()<c.gety()+c.getheight():
                    if p1.getx()+p1.geta()>c.getx() and p1.getx()<c.getx()+c.getwidth()/2:
                        return c.getx()-p1.geta()
                    if p1.getx()+p1.geta()>c.getx()+c.getwidth()/2 and p1.getx()<c.getx()+c.getwidth():
                        return c.getx()+c.getwidth()
    return mover
gamer=1

difficulty=1
difficulties=["Easy","Medium","Hard"]

while gamer:

    layout=[
    [sg.Button("Start Game")],
    [sg.Text("Current difficulty: "+ difficulties[difficulty])],
    [sg.Button("Choose difficulty")],
    [sg.Button("Quit Game")]
]
    window=sg.Window("Game",layout)
    event,values=window.read()

    if event=="Quit Game" or event==sg.WIN_CLOSED:
        window.close()
        break

    active = True
    
    direction=1

    won=0

    mover=0

    jumping=0

    currentscene=1

    check2=0
    check3=0

    Ground_Is_Jumper=0

    clock = pygame.time.Clock()

   

    p1=player(700,500,100,5)
    p1.changeDirection(direction)

    c1=construct(1,600,700,250,40,WEISS)
    c2=construct(1,150,700-140,300,20,WEISS)
    c3=construct(1,1000,700-80,300,20,WEISS)
    c31=construct(1,1450,700,250,40,WEISS)
    
    c4=construct(2,-30,700,180,40,WEISS)
    c41=construct(2,400,700-120,180,20,WEISS)
    c42=construct(2,800,700-240,180,20,WEISS)
    c43=construct(2,1200,700-360,180,20,WEISS)
    c44=construct(2,200,700-480,800,20,WEISS)
    
    c5=construct(3,0,750,1600,40,WEISS)
    c51=construct(3,1550,400,50,400,WEISS)
    c52=construct(3,1550-150,200,20,100,WEISS)
    c53=construct(3,1550-300,500,20,100,WEISS)
    c54=construct(3,1550-450,250,20,100,WEISS)
    c55=construct(3,1550-600,0,20,100,WEISS)
    c56=construct(3,1550-750,300,20,100,WEISS)
    c57=construct(3,1550-900,0,20,100,WEISS)
    c58=construct(3,1550-1050,300,20,100,WEISS)
    c59=construct(3,1550-1200,0,20,100,WEISS)

    c6=construct(4,0,700,200,40,WEISS)
    c61=construct(4,425,0,50,40,WEISS)
    c62=construct(4,750,700,50,40,WEISS)
    c63=construct(4,1200,0,50,40,WEISS)
    c64=construct(4,1550,700,100,40,WEISS)

    c7=construct(5,-100,700,200,40,WEISS)
    c71=construct(5,150,650,50,10,WEISS)
    c72=construct(5,150+40+50,650-60,50,10,WEISS)
    c73=construct(5,150+230-30,650-130,50,10,WEISS)
    c74=construct(5,150+360-65,650-210,50,10,WEISS)
    c75=construct(5,555,650-290,50,10,WEISS)
    c76=construct(5,723,750,50,10,WEISS)
    c77=construct(5,845,750,50,10,WEISS)
    c78=construct(5,723+244,750-150,50,10,WEISS)
    c79=construct(5,723+244+100+20,750-100,50,10,WEISS)
    c791=construct(5,723+244,750-50,50,10,WEISS)
    c792=construct(5,723+244,750-250,50,10,WEISS)
    c793=construct(5,723+244,750-350,50,10,WEISS)
    c794=construct(5,723+244+100+20,750-200,50,10,WEISS)
    c795=construct(5,723+244+100+20,750-300,50,10,WEISS)
    c796=construct(5,1087,750-400,50,10,WEISS)
    c797=construct(5,723+1087-555,750,50,10,WEISS)
    c798=construct(5,845+1087-555,750,50,10,WEISS)
    c799=construct(5,845+1087-555+120,750,500,10,WEISS)
    c781=construct(5,700,20,50,10,WEISS)
    c782=construct(5,700+120+5,20,50,10,WEISS)
    c783=construct(5,700+240+10,20,50,10,WEISS)
    c784=construct(5,700+240+100+15,20+50,50,10,WEISS)
    c785=construct(5,700+240+100+100+20,20+50+50,50,10,WEISS)
    c786=construct(5,700+240+100+100+25+100,20+50+50+50,50,10,WEISS)
    c787=construct(5,700+240+100+100+30+200,20+50+50+50,50,10,WEISS)
    c772=construct(5,700-120-5,20,50,10,WEISS)
    c773=construct(5,700-240-10,20,50,10,WEISS)
    c774=construct(5,700-240-100-15,20+50,50,10,WEISS)
    c775=construct(5,700-240-100-100-20,20+50+50,50,10,WEISS)
    c776=construct(5,700-240-100-100-25-100,20+50+50+50,50,10,WEISS)

    c8=construct(6,-100,750,1050,10,WEISS)
    c81=construct(6,780,0,40,710,WEISS)
    c82=construct(6,100,620-10,100,20,WEISS)
    c83=construct(6,350,620-135-20,100,20,WEISS)
    c84=construct(6,600,620-135-140-30,100,20,WEISS)
    c85=construct(6,350,620-135-140-145-40,100,20,WEISS)
    c86=construct(6,100,620-135-140-145-40,100,20,WEISS)
    c88=construct(6,1500,750,200,10,WEISS)

    c87=construct(6,1000,700,100,10,WEISS)
    c871=construct(6,1165,700-50-3,100,10,WEISS)
    c872=construct(6,1000+165*2,700-100-6,100,10,WEISS)
    c873=construct(6,1000+165,700-150-12,100,10,WEISS)
    c874=construct(6,1000,700-200-18,100,10,WEISS)
    c875=construct(6,1000+165,700-250-24,100,10,WEISS)
    c876=construct(6,1000+165*2,700-300-30,100,10,WEISS)
    c877=construct(6,1000+165,700-350-36,100,10,WEISS)
    c878=construct(6,1000,700-400-42,100,10,WEISS)
    c879=construct(6,1000+165,700-400-42-50,100,10,WEISS)

    c9=construct(7,0,750,75,10,WEISS)
    c91=construct(7,175,300,75,10,WEISS)
    c92=construct(7,175+50+100+100,400,75,10,WEISS)
    c93=construct(7,175+50+100+100+250+100-25-15,550,75,10,WEISS)
    c94=construct(7,175+50+100+100+250+100+150-25+5+75,235,75,10,WEISS)
    c95=construct(7,175+50+100+100+250+100+150-25+5+75+50+200+100-30,400,75,10,WEISS)
    c96=construct(7,1485,700,200,10,WEISS)

    c10=construct(8,-100,750,150,10,WEISS)
    c101=construct(8,700,750,200,10,WEISS)
    c102=construct(8,750,700,100,10,WEISS)
    c103=construct(8,550,600,50,10,WEISS)
    c104=construct(8,350,500,50,10,WEISS)
    c105=construct(8,150,400,50,10,WEISS)
    c106=construct(8,550,200,50,10,WEISS)
    c107=construct(8,350,300,50,10,WEISS)

    c110=construct(9,0,750,100,10,WEISS)
    c111=construct(9,450,750,100,10,WEISS)
    c112=construct(9,900,750,100,10,WEISS)
    c113=construct(9,1350,750,300,10,WEISS)
    c114=construct(9,1350,240,100,10,WEISS)
    c115=construct(9,0,240,125,10,WEISS)
    c116=construct(9,425,240,125,10,WEISS)
    c117=construct(9,900,240,100,10,WEISS)

    c12=construct(10,0,750,200,10,WEISS)
    c121=construct(10,240+33,670+33,100,10,WEISS)
    c122=construct(10,405+33,592+33,100,10,WEISS)
    c123=construct(10,1212+50+40,592+33,100,10,WEISS)
    c124=construct(10,1212+50+40+100,700,300,10,WEISS)
    c125=construct(10,200,50,50,10,WEISS)
    c126=construct(10,275+33,142-33,50,10,WEISS)
    c127=construct(10,386+33,200-33,50,10,WEISS)
    c128=construct(10,1580,0,25,450,WEISS)
    c129=construct(10,800,430,800,20,WEISS)
    c130=construct(10,1460,25,10,50,WEISS)
    c131=construct(10,1460-50-10,25+100+15,10,50,WEISS)
    c132=construct(10,1460-100-20,225+30,10,50,WEISS)

    j1=jumper(7,100,700,50,10,ROT)
    j2=jumper(7,175+75+50,700,50,10,ROT)
    j3=jumper(7,175+50+100+100+75+100,700,50,10,ROT)
    j4=jumper(7,175+50+100+100+250+100+150-25+5,700,50,10,ROT)
    j5=jumper(7,1150+25+5-50+33,700,65,10,ROT)
    j6=jumper(9,1450,700,75,10,ROT)
    j7=jumper(10,75,700,50,10,ROT)
    j8=jumper(10,1460-150-30,325+45,10,50,ROT)
    j9=jumper(10,775+43,325+45-50,10,50,ROT)

    h1=hider(8,100,750,50,10,GRUEN,45,0)
    h2=hider(8,200,750,50,10,GRUEN,45,44)
    h3=hider(8,300,750,50,10,GRUEN,45,0)
    h4=hider(8,400,750,50,10,GRUEN,45,44)
    h5=hider(8,500,750,50,10,GRUEN,45,0)
    h6=hider(8,600,750,50,10,GRUEN,45,44)
    h01=hider(8,950,700,50,10,GRUEN,45,44)
    h11=hider(8,1050,750,50,10,GRUEN,45,0)
    h21=hider(8,1150,700,50,10,GRUEN,45,44)
    h31=hider(8,1250,750,50,10,GRUEN,45,0)
    h41=hider(8,1350,700,50,10,GRUEN,45,44)
    h51=hider(8,1450,750,50,10,GRUEN,45,0)
    h61=hider(8,1550,700,50,10,GRUEN,45,44)
    h7=hider(8,650,650,50,10,GRUEN,45,0)
    h8=hider(8,450,550,50,10,GRUEN,45,0)
    h9=hider(8,250,450,50,10,GRUEN,45,0)
    h10=hider(8,450,250,50,10,GRUEN,45,0)
    h101=hider(8,250,350,50,10,GRUEN,45,0)
    
    m1=moverp(9,150,750,50,10,ORANGE,350,2.5)
    m2=moverp(9,600,750,50,10,ORANGE,800,2.5)
    m3=moverp(9,600+450,750,50,10,ORANGE,800+450,2.5)
    m4=moverp(9,150,240,50,10,ORANGE,350,3.5)
    m5=moverp(9,600,240,50,10,ORANGE,800,2.5)
    m6=moverp(9,600+450,240,50,10,ORANGE,800+450,1.5)
    m7=moverp(10,505+33+50,592+33,40,10,ORANGE,1100-(475/2)+25,2.5)
    m8=moverp(10,1212,592+33,40,10,ORANGE,1100-(475/2)+75-25,2.5)
    m9=moverp(10,520+33-10,200-33,50,10,ORANGE,900,2.5)
    
    movers=[m1,m2,m3,m4,m5,m6,m7,m8,m9]

    jumpers=[j1,j2,j3,j4,j5,j6,j7,j8,j9]

    hiders=[h1,h2,h3,h4,h5,h6,h11,h21,h31,h41,h51,h61,h01,h7,h8,h9,h10,h101]
    
    level1=[c1,c2,c3,c31]
    level2=[c4,c41,c42,c43,c44]
    level3=[c5,c51,c52,c53,c54,c55,c56,c57,c58,c59]
    level4=[c6,c61,c62,c63,c64]
    level5=[c7,c71,c72,c73,c74,c75,c76,c77,c78,c79,c791,c792,c793,c794,c795,c796,c797,c798,c799,c781,c782,c783,c784,c785,c786,c787,c772,c773,c774,c775,c776]
    level6=[c8,c81,c82,c83,c84,c85,c86,c87,c871,c872,c873,c874,c875,c876,c877,c878,c879,c88]
    level7=[c9,c91,c92,c93,c94,c95,c96]
    level8=[c10,c101,c102,c103,c104,c105,c106,c107]
    level9=[c110,c111,c112,c113,c114,c115,c116,c117]
    level10=[c121,c122,c123,c124,c125,c126,c127,c128,c129,c130,c131,c132]
    constructs=[level1,level2,level3,level4,level5,level6,level7,level8,level9,c12,level10]

    for c in constructs[currentscene-1]:
        c.changeDirection(direction)
    
    k1=key(1,200,350,30)
    k2=key(2,80,300,30)
    k3=key(3,120,120,30)
    k4=key(4,1225,200,30)
    k5=key(5,700+240+100+100+30+200+50,20+50+50+50+75,15)
    k6=key(6,1000+165+50,700-400-42-50-50,15)
    k7=key(7,175+50+100+100+250+100-5,550-50,15)
    k8=key(8,575,150,15)
    k9=key(9,50,175,15)
    k90=key(10,1460-150-30-30,325+45+25,15)

    keys=[k1,k2,k3,k4,k5,k6,k7,k8,k9,k90]

    s1=switch(3,1450,600,40,2)
    s2=switch(4,300,600,40,3)
    s3=switch(4,750,100,40,1)
    s4=switch(4,950,700,40,3)
    s5=switch(4,1550,50,40,1)
    s6=switch(5,700,650-290,15,3)
    s7=switch(5,700-240-100-100-25-100-50,20+50+50+50+75,15,1)
    s8=switch(6,765,730,15,5)
    s9=switch(6,100,100,40,6)
    s10=switch(10,175,300,15,3)
    s11=switch(10,1000,50,15,2)
    s12=switch(10,240+33+50,325+45-50,15,1)
    switches=[s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12]

    lastdirection=1
    lastscene=1

    if event=="Choose difficulty":
        window.close()
        layout2=[[sg.Text("Current difficulty: "+ difficulties[difficulty],key="69")],
        [sg.Button("Easy")],
        [sg.Button("Medium")],
        [sg.Button("Hard")],[sg.Button("Back")]]
        window2=sg.Window("Choose difficulty", layout2)
        while 1:
            event,values=window2.read()
            if event==sg.WIN_CLOSED or event=="Back":
                window2.close()
                break
            if event=="Easy":
                difficulty=0
            if event=="Medium":
                difficulty=1
            if event=="Hard":
                difficulty=2
            window2["69"].update("Current difficulty: "+ difficulties[difficulty])


    if event=="Start Game":

        screen = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
        pygame.display.set_caption("Game")

        window.close()

        check1=1

        while active:
            
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    gamer=0
                elif event.type == pygame.KEYDOWN:
                        if event.key==pygame.K_d:
                            mover=1
                        if event.key==pygame.K_a:
                            mover=-1
                        if event.key==pygame.K_SPACE:
                            if direction!=3:
                                if getGround(p1.getx(),p1.gety(),p1.geta(),currentscene,keys)==p1.gety()+p1.geta():
                                    jumping=1
                                    d=Ground_Is_Jumper
                            else:
                                if getGround(p1.getx(),p1.gety(),p1.geta(),currentscene,keys)==p1.gety():
                                    jumping=1
                                    d=Ground_Is_Jumper
                elif event.type == pygame.KEYUP:
                        if event.key==pygame.K_d:
                            mover=0
                        if event.key==pygame.K_a:
                            mover=0
                            
            screen.fill(SCHWARZ)
            screen.blit(BG,(0,0))
            
            mover=changeMover(mover)

            if currentscene==6 and not check1:
                difficulty=2


            if currentscene==5 and p1.getx()>845 and p1.gety()>300 and difficulty==2:
                difficulty=1
                check1=0

            if currentscene==5:
                p1.getsmall()

            for s in switches:
                s.prooftouch(p1.getx(),p1.gety(),p1.geta(),currentscene)
                direction=s.isTouched(direction)

            if direction==5 and not check2:
                p1.getbig()
                check2=1

            if direction==6 and not check3:
                p1.getsmall()
                check3=1

            if currentscene==4 and direction==2:
                direction=1

            

            if lastdirection!=direction:
                if lastscene==currentscene:
                    p1.changeDirection(direction)
                    for k in constructs[currentscene-1]:
                        k.changeDirection(direction)
                    for m in movers:
                        m.changeDirection(direction)
                    for h in hiders:
                        h.changeDirection(direction)
                    for j in jumpers:
                        j.changeDirection(direction)

            
            for hid in hiders:
                hid.ttick()
            
            

            
            for k in keys:
                k.prooftouch(p1.getx(),p1.gety(),p1.geta(),currentscene)
            
            for c in constructs[currentscene-1]:
                if c.getScene()==currentscene:
                    if p1.getx()+p1.geta()>c.getx() and p1.getx()<c.getx()+c.getwidth():
                            if c.gety()+c.getheight()>p1.gety()and c.gety()<p1.gety():
                                jumping=0
                                p1.ResetJump()

            ground=getGround(p1.getx(),p1.gety(),p1.geta(),currentscene,keys)

            for h in hiders:
                h.changeDirection(direction)
            
            if direction==1 or direction==5 or direction==6:
                if p1.gety()>900:
                    active=0
                if p1.getx()>SCREEN_X-p1.geta() and not keys[currentscene-1].isTouched():
                    p1.SetX(SCREEN_X-p1.geta())
                
                if p1.getx()>SCREEN_X and keys[currentscene-1].isTouched() and currentscene!=10:
                    currentscene+=1
                    p1.SceneUp()
                
                if p1.getx()>SCREEN_X and keys[currentscene-1].isTouched() and currentscene==10:
                    won=1
                    active=0

                if p1.getx()+p1.geta()<0 and currentscene!=1:
                    currentscene-=1
                    p1.SceneDown()
                
                if p1.getx()<0 and currentscene==1:
                    p1.SetX(0)
                    
            elif direction==2:
                if p1.getx()>900:
                    active=0
                if p1.gety()>=SCREEN_X-p1.geta() and not keys[currentscene-1].isTouched():
                    p1.SetY(SCREEN_X-p1.geta())
                
                if p1.gety()>SCREEN_X and keys[currentscene-1].isTouched():
                    for c in constructs[currentscene-1]:
                        c.changeDirection(1)
                    currentscene=4
                    direction=1
                    p1.SceneUp()
                
                if p1.gety()+p1.geta()<0 and currentscene!=1:
                    currentscene-=1
                    p1.SceneDown()
                
                if p1.gety()<0 and currentscene==1:
                    p1.SetY(0)
            
            elif direction==3:
                if p1.gety()==-100:
                    active=0
                if p1.getx()>SCREEN_X-p1.geta() and not keys[currentscene-1].isTouched():
                    p1.SetX(SCREEN_X-p1.geta())
                
                if p1.getx()>SCREEN_X and keys[currentscene-1].isTouched():
                    currentscene+=1
                    p1.SceneUp()
                
                if p1.getx()+p1.geta()<0 and currentscene!=1:
                    currentscene-=1
                    p1.SceneDown()
                
                if p1.getx()<0 and currentscene==1:
                    p1.SetX(0)

            for m in movers:
                m.tick()
        
            
            p1.actualise()
            
            p1.move(mover)

            print(p1.getx(),p1.gety())

            
            if jumping:
                if p1.jump(ground,difficulty):
                    jumping=0
            else:
                p1.fall(ground)
            
            p1.paint()

            for m in movers:
                m.paint(currentscene)

            for h in hiders:
                h.paint(currentscene)
            
            for k in keys:
                k.paint(currentscene)
            
            for c in constructs[currentscene-1]:
                c.paint(currentscene)

            for s in switches:
                s.paint(currentscene)
            for j in jumpers:
                j.paint(currentscene)

            lastdirection=direction
            lastscene=currentscene
            
            pygame.display.flip()

            clock.tick(60)
        
        if won:
            notification.notify(title="Du hast gewonnen!",message="Erreichtes Level: "+str(currentscene))
            layout3=[[sg.Text("You won!",)],[sg.Button("Try again")],[sg.Button("Quit game")]]
            window3=sg.Window("You won!",layout3)

            while True:
                event, values=window3.read()
                if event=="Quit game" or event==sg.WIN_CLOSED:
                    active=0
                    gamer=0
                    window3.close()
                    break
                if event=="Try again":
                    won=0
                    window3.close()
                    break
        else:
            notification.notify(title="Du bist gestorben!",message="Erreichtes Level: "+str(currentscene))

        

pygame.quit()