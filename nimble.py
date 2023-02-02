import pygame,time,random,math,os,copy
pygame.init()


class PLAYER:  
    def __init__(self,x,y,keybinds,team,teamcols):
        self.imgwidth = 20
        self.imgheight = 32
        self.originalimages = pygame.image.load(os.path.abspath(os.getcwd())+'\\ken animations.png')
        self.imgscale = 4
        
        self.images = pygame.transform.scale(self.originalimages,(self.originalimages.get_width()*self.imgscale,self.originalimages.get_height()*self.imgscale))
        self.images.set_colorkey((255,255,255))
        temp = pygame.PixelArray(self.images)
        temp.replace((0,162,232),teamcols[team])
        del temp
        self.imgwidth*=self.imgscale
        self.imgheight*=self.imgscale
        self.team = team

        #animation layer, frame, delay, flipped
        self.animationdata = [3,0,120,False]
        self.animationspeeds = [4,6,3,5,6]
        self.animationlengths = [6,6,5,3,3]
        self.speedthrough = [[1,2,4,5],[]]
        self.prevmoving = 0

        self.inputs = [0,0,0,0,0,0]
        self.velocity = [0,0]
        self.speed = 1.5
        self.dashspeed = 30
        self.dashduration = 15
        self.dashcooldown = 40
        self.dashcd = [0,True]
        self.dashon = 0
        self.dashdir = [0,0]

        self.grounded = True
        self.x = x
        self.y = y
        self.keybinds = keybinds
        self.team = team
        
    def draw(self,screen):
        if not self.animationdata[3]:
            screen.blit(self.images,(self.x,self.y),(self.animationdata[0]*self.imgwidth,self.animationdata[1]*self.imgheight,self.imgwidth,self.imgheight))
        else:
            temp = pygame.transform.flip(self.images,True,False)
            temp.set_colorkey((255,255,255))
            screen.blit(temp,(self.x,self.y),((6-self.animationdata[0]-1)*self.imgwidth,self.animationdata[1]*self.imgheight,self.imgwidth,self.imgheight))
    def control(self):
        kprs = pygame.key.get_pressed()
        for a in range(len(self.keybinds)):
            if kprs[self.keybinds[a]]:
                self.inputs[a] = 1
            else:
                self.inputs[a] = 0
    def move(self,mapp):
        self.dashcd[0]-=1
        self.dashon-=1
        
        #dash
        if self.inputs[4]>0.5:
            if self.dashcd[0]<0 and self.dashcd[1]:
                self.dashdir = [(self.inputs[3]-self.inputs[2]),(self.inputs[1]-self.inputs[0])]
                if abs(self.dashdir[0])+abs(self.dashdir[1]) == 0:
                    if self.prevmoving == 0:
                        if self.animationdata[1] == 0:
                            self.dashdir[0] = self.animationdata[0]/3*2-1
                        elif self.animationdata[3]:
                            self.dashdir[0] = 1
                        elif not self.animationdata[3]:
                            self.dashdir[0] = -1
                    else:
                        self.dashdir[0] = self.prevmoving
                self.dashon = self.dashduration
                self.dashcd[0] = self.dashcooldown
                self.dashcd[1] = False
                if self.dashdir[0]>0: self.animationdata = [0,2,5,False]
                else: self.animationdata = [0,2,5,True]
        if self.dashon>0:
            self.velocity[0] = self.dashdir[0]*self.dashspeed
            self.velocity[1] = self.dashdir[1]*self.dashspeed
            self.prevmoving = self.dashdir[0]
            if self.dashdir[0] == 0:
                self.prevmoving = 1
        else:
            pass
        
        #jump
        if self.inputs[0]>0.5:
            if self.grounded:
                self.velocity[1]=-50
        
        #move left/right 
        self.velocity[0]+=self.speed*(self.inputs[3]-self.inputs[2])
        if abs(self.inputs[3]-self.inputs[2])>0.5 and self.grounded and self.dashon<0:
            self.animationdata[1] = 1
            if self.inputs[3]-self.inputs[2]>0.5:
                self.animationdata[3] = False
                self.prevmoving = 1
            elif self.inputs[3]-self.inputs[2]<-0.5:
                self.animationdata[3] = True
                self.prevmoving = -1


        #move character
        self.velocity[1]+=2
        
        self.x+=self.velocity[0]
        t = mapp.collide_x(pygame.Rect(self.x,self.y,self.imgwidth,self.imgheight),self.velocity)
        self.x-=t[0]
        self.velocity[0]+=t[1]
        
        self.y+=self.velocity[1]
        t = mapp.collide_y(pygame.Rect(self.x,self.y,self.imgwidth,self.imgheight),self.velocity)
        self.y-=t[0]
        if t[1]!=0:
            self.velocity[1]+=t[1]
            self.velocity[1] = 0
            self.grounded = t[2]
            self.dashcd[1] = t[2]
        else:
            self.grounded = False


        self.velocity[0]*=0.9
        self.velocity[1]*=0.99

        if abs(self.inputs[3]-self.inputs[2])<0.5 and self.grounded and self.dashon<0:
            if self.prevmoving == 1:
                self.animationdata = [3,0,360,False]
            elif self.prevmoving == -1:
                self.animationdata = [0,0,360,False]
            self.prevmoving = 0
            
        #jump animation
        if (not self.grounded) and self.dashon<0:
            if self.velocity[1]<0:
                if self.velocity[0]>0: self.animationdata = [1,3,2,False]
                else: self.animationdata = [1,3,2,True]
            elif self.animationdata[1]!=4:
                if self.velocity[0]>0:
                    self.animationdata = [0,4,2,False]
                    self.prevmoving = 1
                else:
                    self.animationdata = [0,4,2,True]
                    self.prevmoving = -1
        
    def animate(self):
        if self.animationdata[1] == 0:
            self.animationdata[2]-=1
            if self.animationdata[2] <= 0:
                self.animationdata[0] = (self.animationdata[0]+1)%self.animationlengths[0]
                if (self.animationdata[0] in self.speedthrough[self.animationdata[1]]):
                    self.animationdata[2] = self.animationspeeds[self.animationdata[1]]
                else:
                    self.animationdata[2] = random.randint(120,360)
        elif self.animationdata[1] == 1:
            if self.animationdata[2]>self.animationspeeds[1]:
                self.animationdata[2]=self.animationspeeds[1]
            self.animationdata[2]-=1
            if self.animationdata[2] <= 0:
                self.animationdata[0] = (self.animationdata[0]+1)%self.animationlengths[self.animationdata[1]]
                self.animationdata[2] = self.animationspeeds[self.animationdata[1]]
        elif self.animationdata[1] == 2:
            self.animationdata[2]-=1
            if self.animationdata[2] <= 0:
                self.animationdata[0] = (self.animationdata[0]+1)%6
                if self.animationdata[0] == 0: self.animationdata[0]+=1
                self.animationdata[2] = self.animationspeeds[self.animationdata[1]]
        else:
            if self.animationdata[2]>self.animationspeeds[1]:
                self.animationdata[2]=self.animationspeeds[1]
            self.animationdata[2]-=1
            if self.animationdata[2] <= 0:
                self.animationdata[0] = (self.animationdata[0]+1)%self.animationlengths[self.animationdata[1]]
                self.animationdata[2] = self.animationspeeds[self.animationdata[1]]

class MAP:
    def __init__(self,x,y,w,h,rw,rh):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rw = rw
        self.rh = rh
        self.gridgen()
    def gridgen(self):
        pattern = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0],
                   [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                   [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        self.grid = []
        for b in range(self.h):
            self.grid.append([])
            for a in range(self.w):
                if pattern[b][a] == 1:
                    self.grid[-1].append(pygame.Rect(self.x+self.rw*a,self.y+self.rh*b,self.rw,self.rh))
                else:
                    self.grid[-1].append(0)
             
    def draw(self,screen):
        for b in range(len(self.grid)):
            for a in range(len(self.grid[b])):
                if self.grid[b][a] != 0:
                    pygame.draw.rect(screen,(0,150,0),self.grid[b][a])
    def collide_y(self,pr,pv):
        colw = []
        for b in range(len(self.grid)):
            for a in range(len(self.grid[b])):
                if self.grid[b][a] != 0:
                    if self.grid[b][a].colliderect(pr):
                        if self.grid[b][a].y<pr.y:
                            return -(self.grid[b][a].y+self.grid[b][a].height-pr.y),-pv[1],False
                        else:
                            return pr.y+pr.height-self.grid[b][a].y,-pv[1],True
        return 0,0
    def collide_x(self,pr,pv):
        colw = []
        for b in range(len(self.grid)):
            for a in range(len(self.grid[b])):
                if self.grid[b][a] != 0:
                    if self.grid[b][a].colliderect(pr):
                        if self.grid[b][a].x<pr.x:
                            return -(self.grid[b][a].x+self.grid[b][a].width-pr.x),-pv[0]
                        else:
                            return pr.x+pr.width-self.grid[b][a].x,-pv[0]
        return 0,0
                

class MAIN:
    screen = pygame.display.set_mode((2000, 1200))
    done = False
    clock = pygame.time.Clock()
    def __init__(self):
        teamcols = [(0,162,232),(237,28,36)]
        self.players = [PLAYER(300,500,[pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d,pygame.K_SPACE,pygame.K_e],0,teamcols),
                        PLAYER(800,500,[pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_RETURN,pygame.K_e],0,teamcols)]
        self.map = MAP(0,0,20,12,100,100)
    def gameloop(self):
        while not self.done:             
            self.pyevent()
            self.gametick()
            self.drawall()
            self.clock.tick(60)
        pygame.quit()
        
    def pyevent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                
    def drawall(self):
        self.screen.fill((255,255,255))
        self.map.draw(self.screen)
        for a in self.players:
            a.draw(self.screen)
        pygame.display.flip()
        
    def gametick(self):
        for a in self.players:
            a.control()
            a.move(self.map)
            a.animate()


main = MAIN()
main.gameloop()
