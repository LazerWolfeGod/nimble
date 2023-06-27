import pygame,time,random,math,os,copy,statistics
import ai
pygame.init()

projectileimage = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+'projectiles.png')

def text_objects(text, font, col):
    textSurface = font.render(text, True, col)
    return textSurface, textSurface.get_rect()

def write(x,y,text,col,size,screen,center):
    largeText = pygame.font.SysFont("inkfree",int(size),bold=True)
    TextSurf, TextRect = text_objects(text, largeText, col)
    if center:
        TextRect.center = (int(x),int(y))
    else:
        TextRect.x = int(x)
        TextRect.y = int(y)
##    pixelation = 2.0
##    sc = (TextSurf.get_width(),TextSurf.get_height())
##    tf = pygame.transform.scale(TextSurf,(sc[0]/pixelation,sc[1]/pixelation))
##    TextSurf = pygame.transform.scale(tf,sc)
    
    screen.blit(TextSurf, TextRect)

def maketext(text,col,size):
    largeText = pygame.font.SysFont("inkfree", int(size),bold=True)
    TextSurf, TextRect = text_objects(text, largeText, col)
    return TextSurf

def sigmoid(num,s):
    try:
        return (1/(1+(s**(-(num)))))
    except:
        return 1

def numlimiter(num,h,s):
    return (-s/(x+s/h)+h)

def colliderectbutbetter(rec1,rec2):
    if rec1[0]+rec1[2]>rec2[0] and rec1[0]<rec2[0]+rec2[2] and rec1[1]+rec1[3]>rec2[1] and rec1[1]<rec2[1]+rec2[3]:
        return True
    return False

def button(img,cords,mpos,mprs,mousedata,screen,scale):
    w = img.get_width()/3
    h = img.get_height()
    if pygame.Rect(cords[0]*scale-w/2,cords[1]*scale-h/2,w,h).collidepoint(mpos):
        if mprs[0] and not mousedata[0]:
            screen.blit(img,(cords[0]*scale-w/2,cords[1]*scale-h/2),(w*2,0,w,h))
            return True
        else:
            screen.blit(img,(cords[0]*scale-w/2,cords[1]*scale-h/2),(w,0,w,h))
    else:
        screen.blit(img,(cords[0]*scale-w/2,cords[1]*scale-h/2),(0,0,w,h))
    return False

def slider(img,data,cords,mpos,mprs,mousedata,screen,scale,a):
    acrs = (data[3][2]-data[3][0])/(data[3][1]-data[3][0])
    backimg = data[0]
    bw = backimg.get_width()
    bh = backimg.get_height()
    w = img.get_width()/3
    h = img.get_height()

    screen.blit(backimg,(cords[0]*scale-bw/2,cords[1]*scale-bh/2))
    dispc = (cords[0]*scale-bw/2+(data[2][0]+data[2][2]*acrs-data[1][0])*scale,cords[1]*scale-bh/2+(data[2][1]+data[2][3]*acrs-data[1][1])*scale)
    writec = (dispc[0]+data[1][0]*scale,dispc[1]+data[1][1]*0.27*scale)
    writesize = int(data[1][1]*0.4*scale)
    bd = w
    if data[2][2] == 0:
        bd = h
        writec = (dispc[0]+data[1][0]*0.3*scale,dispc[1]+data[1][1]*scale)
        writesize = int(data[1][0]*0.5*scale)
    if mousedata[1] == a:
        if data[2][2] != 0:
            zto = max([min([((mpos[0]-(cords[0]*scale-bw/2+data[2][0]*scale))/(data[2][2]*scale)),1]),0])
            data[3][2] = int((zto*(data[3][1]-data[3][0])+data[3][0])*20)/20
        elif data[2][3] != 0:
            zto = max([min([((mpos[1]-(cords[1]*scale-bh/2+data[2][1]*scale))/(data[2][3]*scale)),1]),0])
            data[3][2] = round((zto*(data[3][1]-data[3][0])+data[3][0]))
        screen.blit(img,(dispc[0],dispc[1]),(w*2,0,w,h))
        write(writec[0],writec[1],str(data[3][2]).upper(),(72,72,72),writesize,screen,True)
        return 2,data[3][2]
    else:
        if pygame.Rect(dispc[0]+(w-bd),dispc[1]+(h-bd),bd,bd).collidepoint(mpos):
            if mprs[0]:
                screen.blit(img,(dispc[0],dispc[1]),(w*2,0,w,h))
                write(writec[0],writec[1],str(data[3][2]).upper(),(72,72,72),writesize,screen,True)
                return 1,a
            else:
                screen.blit(img,(dispc[0],dispc[1]),(w,0,w,h))
        else:
            screen.blit(img,(dispc[0],dispc[1]),(0,0,w,h))
    write(writec[0],writec[1],str(data[3][2]).upper(),(72,72,72),writesize,screen,True)
    
    return 0,-1 

class PLAYER:
    characteranimationspeed = [[4,6,3,3,6,5,4,6,3],
                               [4,10,5,3,5,7,4,6,7],
                               [5,6,3,5,5,5,5,5,5]]
    characteranimationlengths = [[6,6,5,3,3,4,3,3,9],
                                 [6,8,5,3,4,7,3,1,6],
                                 [6,8,8,1,1,6,1,1,7]]
    characteranimationsizes = [[[20,32],[20,32],[20,32],[14,32],[20,33],[24,32],[16,34],[28,36],[38,42]],
                               [[25,40],[26,44],[29,35],[17,45],[33,45],[33,39],[25,39],[29,47],[58,40]],
                               [[24,34],[26,37],[69,69],[15,39],[27,39],[71,42],[19,34],[40,39],[107,49]]]
    characterparticledata = [[[[8,12],1],[[8,12],1],[[16,15],1]],
                             [[[12,14],1],[[10,15],1],[[13,19],1]],
                             [[[13,14],1],[[33,13],1],[[11,13],1]]]
    characterdamageframes = [[2,3,4,5,6],
                             [5],
                             [5]]
    def __init__(self,x,y,keybinds,team,teamcols,scale,character,attacks,hitbox,imscale,id,ign,characterdic,walkspeed,dashspeed,dashduration,health):
        self.standardhitbox = hitbox
        self.character = character
        self.characterdic = characterdic
        self.originalimages = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+character+' animations.png')
        self.trueimgscale = imscale
        self.imgscale = self.trueimgscale*scale
        self.screenscale = scale
        self.truehitbox = [self.standardhitbox[0]*self.trueimgscale,self.standardhitbox[1]*self.trueimgscale]
        self.hitbox = [self.standardhitbox[0]*self.imgscale,self.standardhitbox[1]*self.imgscale]
        self.images = pygame.transform.scale(self.originalimages,(self.originalimages.get_width()*self.imgscale,self.originalimages.get_height()*self.imgscale))

        self.originalparticlesimage = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+character+' particles.png')
        self.particlesimage = pygame.transform.scale(self.originalparticlesimage,(self.originalparticlesimage.get_width()*self.imgscale,self.originalparticlesimage.get_height()*self.imgscale))
        self.particledata = self.characterparticledata[self.characterdic.index(character)]
        
        
        self.images.set_colorkey((255,255,255))
        temp = pygame.PixelArray(self.images)
        temp.replace((0,162,232),teamcols[team])
        del temp
        temp = pygame.PixelArray(self.particlesimage)
        temp.replace((0,162,232),teamcols[team])
        del temp

        self.flippedimages = pygame.transform.flip(self.images,True,False)
        self.flippedimages.set_colorkey((255,255,255))

        self.drawlower = 0

        self.ign = ign
        self.ignimage = maketext(self.ign,(72,72,72),self.imgscale*5)
        self.ignimagewid = int(self.ignimage.get_width()/2)
        
        self.team = team
        self.teamcols = teamcols

        #animation layer, frame, delay, flipped
        self.animationdata = [3,0,random.randint(60,180),False]
        self.animationspeeds = self.characteranimationspeed[self.characterdic.index(character)]
        self.animationlengths = self.characteranimationlengths[self.characterdic.index(character)]
        self.animationsizes = self.characteranimationsizes[self.characterdic.index(character)]
        self.animationsizeslookup = [0]
        for a in range(len(self.animationsizes)):
            self.animationsizeslookup.append(self.animationsizeslookup[a]+self.animationsizes[a][1])
        self.speedthrough = [[1,2,4,5],[]]
        self.prevmoving = 0
        self.direction = 1

        self.inputs = [0,0,0,0,0,0,0]
        self.velocity = [0,0]
        self.speed = walkspeed
        self.dashspeed = dashspeed
        if attacks!=[]: self.dashcooldown = attacks[1][0][10]
        self.dashduration = dashduration
        self.dashcd = [0,True]
        self.dashon = 0
        self.dashdir = [0,0]
        
        self.attackdata = [0,[0,0]]
        self.attackon = 0
        self.attacks = attacks
        self.attackcd = 0
        self.attackid = random.randint(0,1000000)
        self.damageid = []
        self.stunned = 0
        self.impact = [0,0]
        self.damageframes = self.characterdamageframes[self.characterdic.index(character)]

        self.health = health
        self.maxhealth = self.health

        self.grounded = True
        self.onwall = False
        self.x = x
        self.y = y
        self.keybinds = keybinds
        self.team = team

        self.id = id
        self.aipowered = False
    def resetscale(self,scale):
        self.imgscale = self.trueimgscale*scale
        self.screenscale = scale
        self.ignimage = maketext(self.ign,(72,72,72),self.imgscale*5)
        self.ignimagewid = int(self.ignimage.get_width()/2)
        self.truehitbox = [self.standardhitbox[0]*self.trueimgscale,self.standardhitbox[1]*self.trueimgscale]
        self.hitbox = [self.standardhitbox[0]*self.imgscale,self.standardhitbox[1]*self.imgscale]
        self.images = pygame.transform.scale(self.originalimages,(self.originalimages.get_width()*self.imgscale,self.originalimages.get_height()*self.imgscale))
        self.particlesimage = pygame.transform.scale(self.originalparticlesimage,(self.originalparticlesimage.get_width()*self.imgscale,self.originalparticlesimage.get_height()*self.imgscale))
        self.images.set_colorkey((255,255,255))
        temp = pygame.PixelArray(self.images)
        temp.replace((0,162,232),self.teamcols[self.team])
        del temp
        temp = pygame.PixelArray(self.particlesimage)
        temp.replace((0,162,232),self.teamcols[self.team])
        del temp
        self.flippedimages = pygame.transform.flip(self.images,True,False)
        self.flippedimages.set_colorkey((255,255,255))
    def draw(self,screen,scale,debug,cam):
        if not self.animationdata[3]:
            screen.blit(self.images,((self.x*scale+(self.hitbox[0]-self.animationsizes[self.animationdata[1]][0]*self.imgscale)/2)-cam[0]*scale,(self.y*scale+(self.hitbox[1]-self.animationsizes[self.animationdata[1]][1]*self.imgscale))-cam[1]*scale+self.drawlower*self.imgscale),(self.animationdata[0]*self.animationsizes[self.animationdata[1]][0]*self.imgscale,self.animationsizeslookup[self.animationdata[1]]*self.imgscale,self.animationsizes[self.animationdata[1]][0]*self.imgscale,self.animationsizes[self.animationdata[1]][1]*self.imgscale))
        else:
            screen.blit(self.flippedimages,((self.x*scale+(self.hitbox[0]-self.animationsizes[self.animationdata[1]][0]*self.imgscale)/2)-cam[0]*scale,(self.y*scale+(self.hitbox[1]-self.animationsizes[self.animationdata[1]][1]*self.imgscale))-cam[1]*scale+self.drawlower*self.imgscale),(self.flippedimages.get_width()-((self.animationdata[0]+1)*self.animationsizes[self.animationdata[1]][0]*self.imgscale),self.animationsizeslookup[self.animationdata[1]]*self.imgscale,self.animationsizes[self.animationdata[1]][0]*self.imgscale,self.animationsizes[self.animationdata[1]][1]*self.imgscale))
        pygame.draw.rect(screen,(0,0,0),pygame.Rect((self.x*scale-self.hitbox[0]/4)-cam[0]*scale,(self.y-12)*scale-cam[1]*scale,self.hitbox[0]*1.5,10*scale))
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(((self.x+2)*scale-self.hitbox[0]/4)-cam[0]*scale,(self.y-10)*scale-cam[1]*scale,(self.hitbox[0]*1.5-4*scale)*(self.health/self.maxhealth),6*scale))
        screen.blit(self.ignimage,((self.x)*scale-self.ignimagewid+self.hitbox[0]/2-cam[0]*scale,(self.y-5*self.trueimgscale-15)*scale-cam[1]*scale))
        if debug: pygame.draw.rect(screen,(255,0,0),pygame.Rect(self.x*scale-cam[0]*scale,self.y*scale-cam[1]*scale,self.hitbox[0],self.hitbox[1]),2)
    def control(self,mapp,players,damages):
        kprs = pygame.key.get_pressed()
        for a in range(len(self.keybinds)):
            if kprs[self.keybinds[a]]:
                self.inputs[a] = 1
            else:
                self.inputs[a] = 0
    def get_dir(self,inputs):
        dp = [(inputs[3]-inputs[2]),(inputs[1]-inputs[0])]
        if dp[0] == 0 and dp[1] == 0: dirr = [int(self.direction),0]
        else: dirr = [dp[0]/((dp[0]**2+dp[1]**2)**0.5),dp[1]/((dp[0]**2+dp[1]**2)**0.5)]
        if abs(dirr[0])+abs(dirr[1]) == 0:
            dirr[0] = self.direction
        return dirr
    def move(self,mapp,damages,scale):
        self.dashcd[0]-=1
        self.dashon-=1
        self.attackcd-=1
        self.attackon-=1
        self.stunned-=1

        
        #trigger dash
        if self.inputs[4]>0.5 and self.stunned<0:
            if self.dashcd[0]<0 and self.dashcd[1]:
                self.dashdir = self.get_dir(self.inputs)
                #print(self.dashdir)
                self.dashon = self.dashduration
                self.dashcd[0] = self.dashcooldown
                self.dashcd[1] = False
                if self.dashdir[0]>0: self.animationdata = [0,2,5,False]
                else: self.animationdata = [0,2,5,True]
                self.attackon = -1
                self.attackid = random.randint(0,1000000)
                #print('dash with id:',self.attackid)
                
        #trigger attack
        if (self.inputs[5]>0.5 or self.inputs[6]>0.5) and self.dashon<0 and self.stunned<0:
            if self.attackcd<0:
                if self.onwall:
                    self.direction*=-1
                    self.attackdata[1] = self.get_dir(self.inputs)
                    self.attackdata[1][0]*=-1
                    self.dashon = 4
                    self.dashdir = self.attackdata[1]
                else:
                    self.attackdata[1] = self.get_dir(self.inputs)
                self.attackon = 80
                self.attackdata[0] = 1
                if self.inputs[6]>0.5:
                    self.attackcd = self.attacks[0][0][10]
                    if self.attackdata[1][0]>0: self.animationdata = [0,5,5,False]
                    else: self.animationdata = [0,5,5,True]
                else:
                    self.attackcd = self.attacks[2][0][10]
                    if self.attackdata[1][0]>0: self.animationdata = [0,8,5,False]
                    else: self.animationdata = [0,8,5,True]
                

        #dash stuff if dash active      
        if self.dashon>0:
            self.velocity[0] = self.dashdir[0]*self.dashspeed
            self.velocity[1] = self.dashdir[1]*self.dashspeed
            self.prevmoving = self.dashdir[0]
            if self.dashdir[0] == 0:
                self.prevmoving = 1
            for x in self.attacks[1]:
                damages.append(DAMAGE_AREA(self.x+self.truehitbox[0]/2+x[6][0]*self.trueimgscale*self.dashdir[0],self.y+self.truehitbox[1]/2+x[6][1]*self.trueimgscale*self.dashdir[1],x[0],x[1]*self.trueimgscale,x[2]*self.trueimgscale,x[3],[self.dashdir[0]*x[4],(self.dashdir[1]-0.5)*x[4]],x[5],self.team,self.attackid,scale,[self.dashdir[0]*x[7],self.dashdir[1]*x[7]],[self.dashdir[0]*x[8],(self.dashdir[1]-0.5)*x[8]],x[9]))

        elif self.attackon>0:
            self.prevmoving = self.attackdata[1][0]
            if self.attackdata[1][0] == 0:
                self.prevmoving = 1   
        #jump
        if self.inputs[0]>0.5 and self.stunned<0 and self.dashon<0:
            if self.grounded:
                if self.onwall:
                    self.velocity[0]=20*self.direction*-1
                self.velocity[1]=-50
        
        #move left/right 
        if self.stunned<0:
            self.velocity[0]+=self.speed*(self.inputs[3]-self.inputs[2])
            if abs(self.inputs[3]-self.inputs[2])>0.5 and self.grounded and self.dashon<0 and self.attackon<0:
                if not self.onwall:
                    self.animationdata[1] = 1
                    if self.inputs[3]-self.inputs[2]>0.5:
                        self.animationdata[3] = False
                        self.prevmoving = 1
                        self.direction = 1
                    elif self.inputs[3]-self.inputs[2]<-0.5:
                        self.animationdata[3] = True
                        self.prevmoving = -1
                        self.direction = -1
                else:
                    self.animationdata[1] = 7
                    if self.inputs[3]-self.inputs[2]>0.5:
                        self.animationdata[3] = False
                        self.prevmoving = 1
                        self.direction = 1
                    elif self.inputs[3]-self.inputs[2]<-0.5:
                        self.animationdata[3] = True
                        self.prevmoving = -1
                        self.direction = -1
        else:
            self.drawlower = 0


        #move character
        self.velocity[1]+=2

        if self.onwall:
            self.velocity[1] = min([self.velocity[1],2])
            if self.dashcd[0]<10: self.dashcd[1] = True
        self.y+=self.velocity[1]
        t = mapp.collide_y((self.x,self.y,self.truehitbox[0],self.truehitbox[1]),self.velocity)
        self.y-=t[0]
        if t[1]!=0:
            self.velocity[1]+=t[1]
            self.velocity[1] = 0
            self.grounded = t[2]
            if self.dashcd[0]<10: self.dashcd[1] = t[2]
        else:
            self.grounded = False
        self.x+=self.velocity[0]
        t = mapp.collide_x((self.x,self.y,self.truehitbox[0],self.truehitbox[1]),self.velocity)
        self.x-=t[0]
        self.velocity[0]+=t[1]
        if abs(t[1])>0:
            if self.velocity[1]>0:
                self.onwall = True
                self.grounded = True
        else:
            self.onwall = False


        self.velocity[0]*=0.9
        self.velocity[1]*=0.99

        #standing animation
        if abs(self.inputs[3]-self.inputs[2])<0.5 and self.grounded and self.dashon<0 and self.attackon<0 and self.stunned<0:
            if self.prevmoving == 1:
                self.animationdata = [3,0,360,False]
            elif self.prevmoving == -1:
                self.animationdata = [0,0,360,False]
            self.prevmoving = 0
            
        #jump animation
        if (not self.grounded) and self.dashon<0 and self.attackon<0 and self.stunned<0:
            if self.velocity[1]<0:
                if self.animationdata[1]!=3 and not self.onwall:
                    if self.velocity[0]>0: self.animationdata = [1,3,2,False]
                    else: self.animationdata = [1,3,2,True]
            else:
                if self.animationdata[1]!=4:
                    if self.velocity[0]>0:
                        self.animationdata = [0,4,2,False]
                        self.prevmoving = 1
                    else:
                        self.animationdata = [0,4,2,True]
                        self.prevmoving = -1

        #stunned animation
        if self.stunned>-1:
            self.animationdata[1] = 6
            if self.velocity[0]<0:
                self.animationdata[3] = False
                self.prevmoving = 1
            else:
                self.animationdata[3] = True
                self.prevmoving = -1

        #reset direction
        if abs(self.inputs[3]-self.inputs[2])>0.5:
            if self.inputs[3]-self.inputs[2]<-0.5:
                self.animationdata[3] = True
                self.prevmoving = -1
                self.direction = -1
            else:
                self.animationdata[3] = False
                self.prevmoving = 1
                self.direction = 1
        return damages

    

            
        
    def animate(self,damages,scale,particles,parint,shake):
        self.drawlower = 0
        if self.animationdata[1] == 0:
            self.animationdata[2]-=1
            if self.animationdata[2] <= 0:
                self.animationdata[0] = (self.animationdata[0]+1)%self.animationlengths[0]
                if (self.animationdata[0] in self.speedthrough[self.animationdata[1]]):
                    self.animationdata[2] = self.animationspeeds[self.animationdata[1]]
                else:
                    self.animationdata[2] = random.randint(120,360)
                    self.direction = self.animationdata[0]/3*2-1
                    
        elif self.animationdata[1] == 1:
            if self.animationdata[2]>self.animationspeeds[1]:
                self.animationdata[2]=self.animationspeeds[1]
            self.animationdata[2]-=1
            if self.animationdata[2] <= 0:
                self.animationdata[0] = (self.animationdata[0]+1)%self.animationlengths[self.animationdata[1]]
                self.animationdata[2] = self.animationspeeds[self.animationdata[1]]
                
        elif self.animationdata[1] == 2:
            if self.character == 'alex': self.drawlower = 15
            self.animationdata[2]-=1
            if self.animationdata[2] <= 0:
                self.animationdata[0] = (self.animationdata[0]+1)%self.animationlengths[self.animationdata[1]]
                if self.animationdata[0] == 0: self.animationdata[0]+=1
                self.animationdata[2] = self.animationspeeds[self.animationdata[1]]
                
        elif self.animationdata[1] == 5:
            self.animationdata[2]-=1
            if self.animationdata[0] == self.animationlengths[self.animationdata[1]]-1:
                for x in self.attacks[0]:
                    if not (x[9] == 'spell' or x[9] == 'rock' or x[9] == 'stick'):
                        damages.append(DAMAGE_AREA(self.x+self.truehitbox[0]/2+x[6][0]*self.trueimgscale*(self.animationdata[3]*-2+1),self.y+self.truehitbox[1]/2+x[6][1]*self.trueimgscale,x[0],x[1]*self.trueimgscale,x[2]*self.trueimgscale,x[3],[self.attackdata[1][0]*x[4],(self.attackdata[1][1]-0.5)*x[4]],x[5],self.team,self.attackid,scale,[self.attackdata[1][0]*x[7],(self.attackdata[1][1]-0.5)*x[7]],[self.attackdata[1][0]*x[8],self.attackdata[1][1]*x[8]],x[9]))

            if self.animationdata[2] <= 0:
                self.animationdata[0] = (self.animationdata[0]+1)%self.animationlengths[self.animationdata[1]]
                self.animationdata[2] = self.animationspeeds[self.animationdata[1]]
                if self.animationdata[0] == self.animationlengths[self.animationdata[1]]-1:
                    for x in self.attacks[0]:
                        if x[9] == 'spell' or x[9] == 'rock' or x[9] == 'stick':
                            if x[9] == 'rock' or x[9] == 'stick': vertdir = 1
                            else: vertdir = self.attackdata[1][1]
                            damages.append(DAMAGE_AREA(self.x+self.truehitbox[0]/2+x[6][0]*self.trueimgscale*self.attackdata[1][0],self.y+self.truehitbox[1]/2+x[6][1]*self.trueimgscale*vertdir,x[0],x[1]*self.trueimgscale,x[2]*self.trueimgscale,x[3],[self.attackdata[1][0]*x[4],(self.attackdata[1][1]-0.5)*x[4]],x[5],self.team,self.attackid,scale,[self.attackdata[1][0]*x[7],(self.attackdata[1][1]-0.5)*x[7]],[self.attackdata[1][0]*x[8],self.attackdata[1][1]*x[8]],x[9]))
                if self.animationdata[0] == 0:
                    self.attackon=-1
                    self.attackid = random.randint(0,1000000)
                    self.animationdata[0] = self.animationlengths[self.animationdata[1]]-1
        elif self.animationdata[1] == 8:
            self.animationdata[2]-=1
            if self.animationdata[0] in self.damageframes:
                for x in self.attacks[2]:
                    damages.append(DAMAGE_AREA(self.x+self.truehitbox[0]/2+x[6][0]*self.trueimgscale*(self.animationdata[3]*-2+1),self.y+self.truehitbox[1]/2+x[6][1]*self.trueimgscale,x[0],x[1]*self.trueimgscale,x[2]*self.trueimgscale,x[3],[self.attackdata[1][0]*x[4],(self.attackdata[1][1]-0.5)*x[4]],x[5],self.team,self.attackid,scale,[self.attackdata[1][0]*x[7],(self.attackdata[1][1]-0.5)*x[7]],[self.attackdata[1][0]*x[8],self.attackdata[1][1]*x[8]],x[9]))
                    if x[9] == 'smash':
                        for i in range(int(6*parint)):
                            v = random.gauss(15,3)
                            a = (random.gauss(-0.5,0.05))*math.pi
                            particles.append(PARTICLE(self.x+self.truehitbox[0]/2+x[6][0]*self.trueimgscale*self.attackdata[1][0]+random.gauss(0,10),self.y+self.truehitbox[1]-5,'rock',[v*math.cos(a),v*math.sin(a)],0,0,4))
                        shake = [20,2]
            if self.animationdata[2] <= 0:
                self.animationdata[0] = (self.animationdata[0]+1)%self.animationlengths[self.animationdata[1]]
                self.animationdata[2] = self.animationspeeds[self.animationdata[1]]
                if self.animationdata[0] == 0:
                    self.attackon=-1
                    self.attackid = random.randint(0,1000000)
                    self.animationdata[0] = self.animationlengths[self.animationdata[1]]-1
                
        else:
            if self.animationdata[2]>self.animationspeeds[self.animationdata[1]]:
                self.animationdata[2]=self.animationspeeds[self.animationdata[1]]
            self.animationdata[2]-=1
            if self.animationdata[2] <= 0:
                self.animationdata[0] = (self.animationdata[0]+1)%self.animationlengths[self.animationdata[1]]
                self.animationdata[2] = self.animationspeeds[self.animationdata[1]]
        return damages,particles,shake
    def checkdamage(self,damages,particles,parint):
        for a in damages:
            if a.team!=self.team:
                if not (a.id in self.damageid):
                    te = a.checkhit(pygame.Rect(self.x,self.y,self.truehitbox[0],self.truehitbox[1]))
                    if te[0]:
                        a.piercing-=1
                        self.velocity[0]+=te[2][0]
                        self.velocity[1]+=te[2][1]
                        self.health-=te[1]
                        self.stunned = te[3]
                        self.damageid.append(a.id)
                        self.animationdata[0] = 0
                        imp = te[4]
                        self.impact = [math.sqrt(imp[0]**2+imp[1]**2),0]
                        if imp[0] == 0:
                            if imp[1]>0:
                                self.impact[1] = math.pi/2
                            else:
                                self.impact[1] = math.pi*3/2
                        else:
                            self.impact[1] = math.atan(imp[1]/imp[0])
                            if imp[0]<0:
                                self.impact[1]+=math.pi
                        for b in range(int(15*parint)):
                            ang = self.impact[1]+random.gauss(0,0.3)
                            forc = self.impact[0]+random.gauss(0,4)
                            particles.append(PARTICLE(self.x+self.truehitbox[0]/2,self.y+self.truehitbox[1]/2,'blood',[forc*math.cos(ang),forc*math.sin(ang)],self.particledata,self.particlesimage,self.imgscale))
        return particles
    def death(self,particles,parint):
        limbdata = [['limb head',(0,-10)],['limb arm',(5,0)],['limb leg',(3,10)],['limb arm',(-5,0)],['limb leg',(-3,-10)]]
        limbmake = []
        for a in range(int(len(limbdata)*parint)):
            limbmake.append(limbdata[a%len(limbdata)][:])
        for a in range(len(limbmake)):
            ang = self.impact[1]+random.gauss(0,0.3)
            forc = self.impact[0]+random.gauss(0,4)
            particles.append(PARTICLE(self.x+self.truehitbox[0]/2+limbmake[a][1][0]*self.imgscale,self.y+self.truehitbox[1]/2+limbmake[a][1][1]*self.imgscale,limbmake[a][0],[forc*math.cos(ang),forc*math.sin(ang)],self.particledata,self.particlesimage,self.imgscale))
        return particles

class AIPOWEREDPLAYER(PLAYER):
    def __init__(self,x,y,keybinds,team,teamcols,scale,character,attacks,hitbox,imscale,id,ign,characterdic,walkspeed,dashspeed,dashduration,health):
        super().__init__(x,y,keybinds,team,teamcols,scale,character,attacks,hitbox,imscale,id,ign,characterdic,walkspeed,dashspeed,dashduration,health)
        self.aipowered = True
        self.net = ai.AI(30+330*id,30,300,200,10,22,7,2,'none')
    def control(self,mapp,players,damages):
        kprs = pygame.key.get_pressed()
        for a in range(len(self.keybinds)):
            if kprs[self.keybinds[a]]: self.inputs[a] = 1
            else: self.inputs[a] = 0
        inp = self.get_inputs(mapp,players,damages)
        
        self.inputs = self.net.processinput(inp)

    def get_inputs(self,mapp,players,damages):
        inputs = []
        
        #data about self
        #player velocity
        #player animation type, and progression through the animation if it is an attack or dash
        inputs.append(sigmoid(self.velocity[0],1.2))
        inputs.append(sigmoid(self.velocity[1],1.2))
        inputs.append(self.animationdata[1]/8)
        if self.animationdata[1] in [2,5,8]: inputs.append(self.animationdata[0]/(self.animationlengths[self.animationdata[1]]-1))
        else: inputs.append(0)


        #other player input
        #the relative locations of each player in comparison to self
        #player velocity
        #player animation type, and progression through the animation if it is an attack or dash
        for a in range(4):
            if a<len(players):
                if players[a].id != self.id:
                    inputs.append(sigmoid(players[a].x-self.x,1.1))
                    inputs.append(sigmoid(players[a].y-self.y,1.1))
                    inputs.append(sigmoid(players[a].velocity[0],1.2))
                    inputs.append(sigmoid(players[a].velocity[0],1.2))
                    inputs.append(players[a].animationdata[1]/8)
                    if players[a].animationdata[1] in [2,5,8]: inputs.append(players[a].animationdata[0]/(players[a].animationlengths[players[a].animationdata[1]]-1))
                    else: inputs.append(0)
            else:
                for b in range(6): inputs.append(0)


        #damages input
        #gives data about the closest 3 damage aoes with non repeated ids, closest of repeated ids is given
        #gives relative cordinates, same method as relative player cords
        #gives size of aoe
        #gives damage of aoe
        
        
        #map input
        #7x7 grid around player 0 for nothing there, 1 for a block
        #the cordinates of player on the block it is on

        
        return inputs
    
        
        
             

class MAP:
    def __init__(self,x,y,rw,rh,scale,mapid):
        self.x = x
        self.y = y
        self.rw = rw
        self.rh = rh
        self.originalimage = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+'dirt.png')
        self.playerspawnlocplayers = [PLAYER(0,0,[],a,[(0,162,232),(237,28,36),(0,175,80),(163,73,164)],scale,'ken',[],[10,32],int(4*rh/100),0,'player '+str(a+1),['ken'],0,0,0,1) for a in range(4)]
        self.mapid = mapid
        self.playerspawnlocdraw = False
        self.loadmaps()
        self.regenpattern(scale)
    def loadmaps(self):
        with open('maps.txt','r') as f:
            lines = f.readlines()
        self.mappatterns = []
        for a in lines:
            b = a.split('\n')[0]
            if b[0] == ';':
                self.mappatterns.append([])
            else:
                c = b.split(',')
                d = []
                for e in c:
                    if e in ['p1','p2','p3','p4']:d.append(e)
                    else: d.append(int(e))
                self.mappatterns[-1].append(d)
    def gridgen(self):
        pattern = copy.deepcopy(self.pattern)
        for a in range(len(pattern)):
            pattern[a].insert(0,0)
            pattern[a].append(0)
        pattern.insert(0,[0 for a in range(len(pattern[0]))])
        pattern.append([0 for a in range(len(pattern[0]))])
        self.grid = []
        self.playercords = [[] for a in range(4)]
        for b in range(len(pattern)):
            self.grid.append([])
            for a in range(len(pattern[b])):
                img = self.imgmake(a,b,pattern)
                if pattern[b][a]!=0 and not(pattern[b][a] in ['p1','p2','p3','p4']):
                    self.grid[-1].append([pygame.Rect(self.truex-self.patterncenter[0]*self.rw+self.rw*(a-1),self.truey-self.patterncenter[1]*self.rh+self.rh*(b-1),self.rw,self.rh),img])
                else:
                    self.grid[-1].append([0,img])
                if pattern[b][a] == 'p1': self.playercords[0] = [self.truex-self.patterncenter[0]*self.rw+self.rw*(a-0.5),self.truey-self.patterncenter[1]*self.rh+self.rh*b]
                elif pattern[b][a] == 'p2': self.playercords[1] = [self.truex-self.patterncenter[0]*self.rw+self.rw*(a-0.5),self.truey-self.patterncenter[1]*self.rh+self.rh*b]
                elif pattern[b][a] == 'p3': self.playercords[2] = [self.truex-self.patterncenter[0]*self.rw+self.rw*(a-0.5),self.truey-self.patterncenter[1]*self.rh+self.rh*b]
                elif pattern[b][a] == 'p4': self.playercords[3] = [self.truex-self.patterncenter[0]*self.rw+self.rw*(a-0.5),self.truey-self.patterncenter[1]*self.rh+self.rh*b]
        for a in range(len(self.playerspawnlocplayers)):
            if self.playercords[a]!=[]:
                self.playerspawnlocplayers[a].x = self.playercords[a][0]-5*int(4*self.rh/100)
                self.playerspawnlocplayers[a].y = self.playercords[a][1]-32*int(4*self.rh/100)

        #[spawncords[a][0]-self.characters[self.characterdic.index(self.playercreationtabs[a].character)][2][0]/2,spawncords[a][1]-self.characters[self.characterdic.index(self.playercreationtabs[a].character)][2][1]*4]
    def regenpattern(self,scale):
        if self.mapid == -1:
            self.pattern = [[0]]
        else:
            self.pattern = copy.deepcopy(self.mappatterns[self.mapid])
        self.w = len(self.pattern[0])
        self.h = len(self.pattern)
        self.patterncenter = [round((self.w)/2),round((self.h)/2)]
        self.truex = self.x+(self.patterncenter[0])*self.rw
        self.truey = self.y+(self.patterncenter[1])*self.rh
        self.resetscale(scale)
        
    def imgmake(self,x,y,pattern):
        img = pygame.Surface((self.rw,self.rh))
        img.fill((255,255,255))
        blitted = False
        for b in range(len(self.images),0,-1):
            if pattern[y][x] == b:
                img.blit(self.images[b-1][0],(0,0))
                blitted = True
            else:
                aroundmap = [[0,-1],[-1,0],[1,0],[0,1]]
                for i,a in enumerate(aroundmap):
                    if y+a[1]>-1 and y+a[1]<len(pattern) and x+a[0]>-1 and x+a[0]<len(pattern[0]):
                        if pattern[y+a[1]][x+a[0]] == b:
                            img.blit(self.images[b-1][1][i],(0,0))
                            blitted = True
                        
        img.set_colorkey((255,255,255))
        if not blitted: img = 0
        return img
            
        
                                
    def resetscale(self,scale):
        pixels = 50
        imgdata = [[1],[1],[1],[1]]
        self.imagescaled = pygame.transform.scale(self.originalimage,(self.originalimage.get_width()*scale*self.rw/pixels,self.originalimage.get_height()*scale*self.rh/pixels))
        self.images = []

        for i,a in enumerate(imgdata):
            image = pygame.Surface((self.rw*scale,self.rh*scale))
            image.blit(self.imagescaled,(0,0),(0*self.rw*scale,i*2*self.rh*scale,self.rw*scale,self.rh*scale))
            self.images.append([image,[]])
            for a in range(4):
                img = pygame.Surface((self.rw*scale,self.rh*scale))
                img.blit(self.imagescaled,(0,0),(a*self.rw*scale,self.rh*scale*(i*2+1),self.rw*scale,self.rh*scale))
                img.set_colorkey((255,255,255))
                self.images[-1][1].append(img)
        self.gridgen()

    def center(self,centeraround):
        self.truex = centeraround.x+centeraround.width/2
        self.truey = centeraround.y+centeraround.height/2
        self.w = len(self.pattern[0])
        self.h = len(self.pattern)
        self.patterncenter = [round((self.w)/2),round((self.h)/2)] 
        self.gridgen()
             
    def draw(self,screen,scale,cam):
        self.x = self.truex-self.patterncenter[0]*self.rw
        self.y = self.truey-self.patterncenter[1]*self.rh
        self.topleftdrawing = [self.x-self.rw,self.y-self.rh]
        if self.playerspawnlocdraw:
            for a in range(len(self.playerspawnlocplayers)):
                if self.playercords[a] != []:
                    self.playerspawnlocplayers[a].draw(screen,scale,False,cam)
        for b in range(len(self.grid)):
            for a in range(len(self.grid[b])):
                if self.grid[b][a][1] != 0:
                    screen.blit(self.grid[b][a][1],((self.topleftdrawing[0]+a*self.rw-cam[0])*scale,(self.topleftdrawing[1]+b*self.rh-cam[1])*scale))

    def collide_y(self,pr,pv):
        colw = []
        for b in range(len(self.grid)):
            for a in range(len(self.grid[b])):
                if self.grid[b][a][0] != 0:
                    if colliderectbutbetter((self.grid[b][a][0].x,self.grid[b][a][0].y,self.grid[b][a][0].width,self.grid[b][a][0].height),(pr)):
                        if self.grid[b][a][0].y+self.grid[b][a][0].height<pr[1]+pr[3]:
                            return -(self.grid[b][a][0].y+self.grid[b][a][0].height-pr[1]),-pv[1],False
                        elif self.grid[b][a][0].y>pr[1]:
                            return pr[1]+pr[3]-self.grid[b][a][0].y,-pv[1],True
                        else:
                            if pv[1]>0: return pr[1]+pr[3]-self.grid[b][a][0].y,-pv[1],True
                            else: return -(self.grid[b][a][0].y+self.grid[b][a][0].height-pr[1]),-pv[1],False
        return 0,0
    def collide_x(self,pr,pv):
        colw = []
        for b in range(len(self.grid)):
            for a in range(len(self.grid[b])):
                if self.grid[b][a][0] != 0:
                    if colliderectbutbetter((self.grid[b][a][0].x,self.grid[b][a][0].y,self.grid[b][a][0].width,self.grid[b][a][0].height),(pr)):
                        if self.grid[b][a][0].x+self.grid[b][a][0].width<pr[0]+pr[2]:
                            return -(self.grid[b][a][0].x+self.grid[b][a][0].width-pr[0]),-pv[0]
                        elif self.grid[b][a][0].x>pr[0]:
                            return pr[0]+pr[2]-self.grid[b][a][0].x,-pv[0]
                        else:
                            if pv[0]>0: return pr[0]+pr[2]-self.grid[b][a][0].x,-pv[0]
                            else: return -(self.grid[b][a][0].x+self.grid[b][a][0].width-pr[0]),-pv[0]
        return 0,0

class DAMAGE_AREA:
    def __init__(self,x,y,shape,data1,data2,damage,kb,stun,team,idd,scale,impact,vel,typ):
        self.x = x
        self.y = y
        self.shape = shape
        self.damage = damage
        self.kb = kb
        self.velocity = vel
        self.stun = stun
        self.team = team
        self.piercing = -1
        self.impact = impact
        if typ == 'dash': self.timer = 3
        elif typ == 'spell' or typ == 'rock' or typ == 'stick':
            self.projid = ['spell','rock','stick'].index(typ)
            if typ == 'spell':
                self.timer = 100
            elif typ == 'rock':
                self.timer = 180
                self.velocity[1]-=4
            else:
                self.timer = 100
                self.velocity[1]-=6
            self.baseaninfo = [[3,[17,17],10,0],[3,[19,19],5,17],[1,[66,66],5,36]]
            self.aninfo = self.baseaninfo[self.projid]
            self.projimage = projectileimage#pygame.image.load(os.path.abspath(os.getcwd())+'\\'+'projectiles.png')
            self.image = pygame.Surface((self.aninfo[1][0]*self.aninfo[0],self.aninfo[1][1]))
            self.image.blit(self.projimage,(0,0),(0,self.aninfo[3],self.aninfo[1][0]*self.aninfo[0],self.aninfo[1][1]))
            self.image = pygame.transform.scale(self.image,(self.image.get_width()*scale*2,self.image.get_height()*scale*2))
            self.aninfo[1] = [self.aninfo[1][0]*2*scale,self.aninfo[1][1]*(2)*scale]
            self.image.set_colorkey((255,255,255))
            self.animationdata = [0,6]
            if vel[0] == 0:
                if vel[1]>0:
                    self.angle = math.pi/2
                else:
                    self.angle = math.pi*3/2
            else:
                self.angle = math.atan(vel[1]/vel[0])
                if vel[0]<0:
                    self.angle+=math.pi
                self.piercing = 1
        else: self.timer = 10
        self.typ = typ
        self.id = idd
        if self.shape == 'circle':
            self.radius = data1
        elif self.shape == 'rect':
            self.width = data1
            self.height = data2
            self.x-=self.width/2
            self.y-=self.height/2
        self.genshape(scale)
    def genshape(self,scale):
        if self.shape == 'circle':
            self.surf = pygame.Surface((self.radius*2*scale, self.radius*2*scale), pygame.SRCALPHA)    
            pygame.draw.circle(self.surf, (255, 0, 0, 50), (self.radius*scale, self.radius*scale), self.radius*scale)
        elif self.shape == 'rect':
            self.surf = pygame.Surface((self.width*scale, self.height*scale), pygame.SRCALPHA)    
            self.surf.fill((255, 0, 0, 50))
    def move(self,mapp,particles,parint,shake):
        self.x+=self.velocity[0]
        self.y+=self.velocity[1]
        if self.x>mapp.x+mapp.w*mapp.rw+300 or self.x<mapp.x-300 or self.y>mapp.y+mapp.h*mapp.rh+300 or self.y<mapp.y-1000:
            return particles,True,shake
        if self.typ == 'spell':
            pnum = random.random()*3*parint
            if random.random()<pnum%1: pnum = int(pnum+1)
            else: pnum = int(pnum)
            for i in range(pnum):
                v = random.gauss(10,3)
                a = self.angle+random.gauss(0,0.1)
                particles.append(PARTICLE(self.x+random.randint(-6,6),self.y+random.randint(-6,6),'spark',[v*math.cos(a),v*math.sin(a)],0,0,4))
            t = mapp.collide_x((self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2),[0])
            if t[0] != 0 or self.piercing == 0:
                return particles,True,shake
        elif self.typ == 'rock':
            self.velocity[1]+=0.5
            pnum = random.random()*parint
            if random.random()<pnum%1: pnum = int(pnum+1)
            else: pnum = int(pnum)
            for i in range(pnum):
                v = random.gauss(0,3)
                a = self.angle+math.pi+random.gauss(0,0.1)
                particles.append(PARTICLE(self.x+random.randint(-6,6),self.y+random.randint(-6,6),'rock',[v*math.cos(a),v*math.sin(a)],0,0,4))
            t = mapp.collide_x((self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2),[0])
            if t[0] != 0 or self.piercing == 0:
                for i in range(int(40*parint)):
                    v = random.gauss(15,3)
                    a = random.random()*math.pi*2
                    particles.append(PARTICLE(self.x+random.randint(-6,6),self.y+random.randint(-6,6),'rock',[v*math.cos(a),v*math.sin(a)],0,0,4))
                shake = [10,1.5]
                return particles,True,shake
            
        if self.typ == 'stick':
            self.velocity[1]+=0.4
            hitboxlimiter = 0.4
            t = mapp.collide_x((self.x-self.radius*hitboxlimiter,self.y-self.radius*hitboxlimiter,self.radius*2*hitboxlimiter,self.radius*2*hitboxlimiter),[0])
            if t[0] != 0 or self.piercing == 0:
                return particles,True,shake
            
        return particles,False,shake
    def spelldraw(self,screen,scale,cam):
        self.animationdata[1]-=1
        if self.animationdata[1] == 0:
            self.animationdata[1] = self.aninfo[2]
            self.animationdata[0] = (self.animationdata[0]+1)%self.aninfo[0]
        if self.typ == 'stick':
            temp = pygame.Surface((self.aninfo[1][0],self.aninfo[1][1]))
            temp.fill((255,255,255))
            temp.blit(self.image,(0,0),(self.aninfo[1][0]*self.animationdata[0],0,self.aninfo[1][0],self.aninfo[1][1]))
            temp2 = pygame.transform.rotate(temp,math.atan(self.velocity[0]/self.velocity[1])/math.pi*180+90-16.858)
            temp2.set_colorkey((255,255,255))
            screen.blit(temp2,((self.x-cam[0])*scale-temp2.get_width()*0.5,(self.y-cam[1])*scale-temp2.get_height()*0.5))
        else: 
            if self.velocity[0]>0:
                screen.blit(self.image,((self.x-cam[0])*scale-self.aninfo[1][0]*0.5,(self.y-cam[1])*scale-self.aninfo[1][1]*0.5),(self.aninfo[1][0]*self.animationdata[0],0,self.aninfo[1][0],self.aninfo[1][1]))
            else:
                temp = pygame.transform.flip(self.image,True,False)
                temp.set_colorkey((255,255,255))
                screen.blit(temp,((self.x-cam[0])*scale-self.aninfo[1][0]*0.5,(self.y-cam[1])*scale-self.aninfo[1][1]*0.5),(temp.get_width()-self.aninfo[1][0]*(self.animationdata[0]+1),0,self.aninfo[1][0],self.aninfo[1][1]))

    def draw(self,screen,scale,cam):
        if self.shape == 'circle': c = ((self.x-self.radius-cam[0])*scale,(self.y-self.radius-cam[1])*scale)
        elif self.shape == 'rect': c = ((self.x-cam[0])*scale,(self.y-cam[1])*scale)
        screen.blit(self.surf,c)
    def checkhit(self,pr):
        if self.shape == 'circle':
            if (self.x>pr.x and self.x<pr.x+pr.width) or (self.y>pr.y and self.y<pr.y+pr.height):
                if pr.colliderect(pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)):
                    return True,self.damage,self.kb,self.stun,self.impact
            else:
                corners = [(pr.x,pr.y),(pr.x+pr.width,pr.y),(pr.x+pr.width,pr.y+pr.height),(pr.x,pr.y+pr.height)]
                for a in corners:
                    if math.sqrt((a[0]-self.x)**2+(a[1]-self.y)**2)<self.radius:
                        return True,self.damage,self.kb,self.stun,self.impact
                
        else:
            if pr.colliderect(pygame.Rect(self.x,self.y,self.width,self.height)):
                return True,self.damage,self.kb,self.stun,self.impact
        return False,0,0,0,0

class PARTICLE:
    def __init__(self,x,y,typ,velocity,imgdata,img,imgscale):
        self.x = x
        self.y = y
        self.angle = random.random()*math.pi
        self.typ = typ
        self.imgdata = imgdata
        self.imgscale = imgscale
        self.img = img
        self.bounce = 0
        if self.typ == 'blood':
            self.col = (random.randint(200,255),random.randint(0,50),random.randint(0,50))
            self.size = random.randint(6,10)
            self.drag = random.random()/10+0.85
            self.timer = int(self.size*10)
            self.bounce = -0.2
        elif self.typ == 'spark':
            self.col = (255,random.randint(100,150),random.randint(0,50))
            self.size = random.randint(6,10)
            self.drag = random.random()/10+0.85
            self.timer = self.size*4
        elif self.typ == 'rock':
            r = random.randint(100,200)
            self.col = (r,r,r)
            self.size = random.randint(6,10)
            self.drag = random.random()/10+0.85
            self.timer = self.size*4
            self.bounce = -0.8
        elif 'limb' in self.typ:
            if 'head' in self.typ:  
                self.animationdata = [0,2]
                self.drag = 0.99
            elif 'leg' in self.typ:
                self.animationdata = [0,0]
                self.drag = random.random()/10+0.85
            else:
                self.animationdata = [0,1]
                self.drag = random.random()/10+0.85
            self.animationsizeslookup = [0]
            for a in range(len(self.imgdata)):
                self.animationsizeslookup.append(self.animationsizeslookup[a]+self.imgdata[a][0][1])
            ns = 1
            self.imgscale*=ns
            self.img = pygame.transform.scale(self.img,(img.get_width()*ns,img.get_height()*ns))
            temp = pygame.Surface((self.imgdata[self.animationdata[1]][0][0]*self.imgdata[self.animationdata[1]][1]*imgscale,self.imgdata[self.animationdata[1]][0][1]*imgscale))
            temp.blit(self.img,(0,0),(0,self.animationsizeslookup[self.animationdata[1]]*self.imgscale,self.imgdata[self.animationdata[1]][0][0]*self.imgdata[self.animationdata[1]][1]*imgscale,self.imgdata[self.animationdata[1]][0][1]*imgscale))
            self.img = temp
            self.size = self.imgdata[self.animationdata[1]][0][1]*imgscale
            self.timer = int(self.size*10)
            self.bounce = -0.5
            
        self.ttimer = self.timer
        self.velocity = velocity
        
    def draw(self,screen,scale,cam):
        if 'limb' in self.typ:
            temp = pygame.Surface((self.imgdata[self.animationdata[1]][0][0]*self.imgscale,self.imgdata[self.animationdata[1]][0][1]*self.imgscale))
            temp.blit(self.img,(0,0),(self.animationdata[0]*self.imgdata[self.animationdata[1]][0][0]*self.imgscale,0,self.imgdata[self.animationdata[1]][0][0]*self.imgscale,self.imgdata[self.animationdata[1]][0][1]*self.imgscale))
            rot = pygame.transform.rotate(temp,self.angle)
            rot.set_colorkey((255,255,255))
            screen.blit(rot,(self.x*scale-rot.get_width()/2-cam[0]*scale,self.y*scale-rot.get_height()/2-cam[1]*scale))
        else:
            pygame.draw.circle(screen,self.col,(self.x*scale-cam[0]*scale,self.y*scale-cam[1]*scale),self.size*scale*(self.timer/self.ttimer))
    def move(self,mapp,particlephysics):
        self.timer-=1
        if 'limb' in self.typ:
            self.animationdata[0] = int(self.imgdata[self.animationdata[1]][1]*(1-(self.timer/self.ttimer)))
            if self.animationdata[0] == self.imgdata[self.animationdata[1]][1]:
                return True
        else:
            if self.timer<0:
                return True
        if self.typ != 'spark': self.velocity[1]+=1
        self.angle-=self.velocity[0]

        if 'limb' in self.typ:
            if 'head' in self.typ:
                mul = 0.8
            else:
                mul = 1
        else:
            mul = (self.timer/self.ttimer)
        
        self.x+=self.velocity[0]
        if particlephysics:
            t = mapp.collide_x((self.x-self.size/2*mul,self.y-self.size/2*mul,self.size*mul,self.size*mul),self.velocity)
            self.x-=t[0]
            if abs(t[1])>0:
                self.velocity[0]*=self.bounce
                self.velocity[1]*=self.drag
            
        self.y+=self.velocity[1]
        if particlephysics:
            t = mapp.collide_y((self.x-self.size/2*mul,self.y-self.size/2*mul,self.size*mul,self.size*mul),self.velocity)
            self.y-=t[0]
            if abs(t[1])>0:
                self.velocity[1]*=self.bounce
                self.velocity[0]*=self.drag
        return False

class WALLPAPER:
    def __init__(self,scale):
        self.originaltitle = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+'nimble title.png')
        self.originalcloud = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+'cloud.png')
        self.imgsize = [self.originalcloud.get_width(),self.originalcloud.get_height()]
        self.genbackground(scale)
    def genbackground(self,scale):
        self.title = pygame.transform.scale(self.originaltitle,(self.originaltitle.get_width()*scale,self.originaltitle.get_height()*scale))
        self.cloud = pygame.transform.scale(self.originalcloud,(self.originalcloud.get_width()*scale,self.originalcloud.get_height()*scale))
        self.cloud.set_colorkey((255,255,255))
        self.title.set_colorkey((255,255,255))
        self.clouds = []
        for a in range(12):
            cl = [random.randint(0,2000-self.imgsize[0]),random.randint(0,1200-self.imgsize[1]),(random.random()+0.1)/2,self.imgsize]
            while self.overlap_check(cl):
                cl = [random.randint(0,2000-self.imgsize[0]),random.randint(0,1200-self.imgsize[1]),(random.random()+0.1)/2,self.imgsize]
            self.clouds.append(cl)
    def resetscale(self,scale):
        self.title = pygame.transform.scale(self.originaltitle,(self.originaltitle.get_width()*scale,self.originaltitle.get_height()*scale))
        self.cloud = pygame.transform.scale(self.originalcloud,(self.originalcloud.get_width()*scale,self.originalcloud.get_height()*scale))
        self.cloud.set_colorkey((255,255,255))
        self.title.set_colorkey((255,255,255))
    def draw(self,screen,display,scale):
        screen.fill((79,173,245))
        for a in self.clouds:
            screen.blit(self.cloud,(a[0]*scale,a[1]*scale))
            a[0]+=a[2]
            if a[0]>2000:
                a[0] = -self.imgsize[0]
                a[1] = random.randint(0,1200-self.imgsize[1])
                a[2] = (random.random()+0.1)/2
        if display == 'menu':
            screen.blit(self.title,(1000*scale-self.title.get_width()/2,200*scale-self.title.get_height()/2))
    def overlap_check(self,cloud):
        for a in self.clouds:
            if pygame.Rect(a[0],a[1],a[3][0],a[3][1]).colliderect(cloud[0],cloud[1],cloud[3][0],cloud[3][1]):
                return True
        return False

class PLAYERCREATIONTAB:
    def __init__(self,scale,team,teamcols,placement,playernum,characterdic,aicontrolled):
        self.y = 30
        self.x = 30+500*team
        self.seperation = 30
        self.team = team
        self.aicontrolled = aicontrolled
        self.playernum = playernum
        self.playername = 'player '+str(self.playernum)
        self.character = characterdic[(playernum-1)%len(characterdic)]
        self.characterdic = characterdic
        self.teamcols = teamcols
        self.backingsize = (432,938)
        self.buttondata = [[3,[64,64],0],[3,[64,64],64],[3,[322,82],128],[3,[296,124],210],[3,[286,82],334],[1,[130,106],416]]
        
        self.origbackings = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+'player creation tab.png')
        self.backingimg = pygame.transform.scale(self.origbackings,(self.origbackings.get_width()*2,self.origbackings.get_height()*2))
        
        self.origbuttons = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+'player creation buttons.png')
        self.buttonimg = pygame.transform.scale(self.origbuttons,(self.origbuttons.get_width()*2,self.origbuttons.get_height()*2))
        self.resetscalepos(scale,placement)
    def resetscalepos(self,scale,pm):
        self.x = 1000-(pm[1]*(self.backingsize[0]+self.seperation)-self.seperation)/2+(self.backingsize[0]+self.seperation)*pm[0]
        self.x = self.seperation+(self.backingsize[0]+self.seperation)*pm[0]
        self.idledude = PLAYER(self.x+self.backingsize[0]/2,self.y+200,[],self.team,self.teamcols,scale,self.character,[],[0,32],8,0,'',self.characterdic,1,1,1,1)
        self.backings = []
        for a in range(len(self.teamcols)):
            ts = pygame.Surface(self.backingsize)
            ts.blit(self.backingimg,(0,0),(self.backingsize[0]*a,0,self.backingsize[0],self.backingsize[1]))
            ts.set_colorkey((255,255,255))
            ts = pygame.transform.scale(ts,(ts.get_width()*scale,ts.get_height()*scale))
            self.backings.append(ts)
        self.buttonsurfaces = [pygame.Surface((a[1][0]*a[0],a[1][1])) for a in self.buttondata]
        for a in range(len(self.buttonsurfaces)):
            self.buttonsurfaces[a].blit(self.buttonimg,(0,0),(0,self.buttondata[a][2],self.buttondata[a][1][0]*self.buttondata[a][0],self.buttondata[a][1][1]))
            self.buttonsurfaces[a].set_colorkey((255,255,255))
            self.buttonsurfaces[a] = pygame.transform.scale(self.buttonsurfaces[a],(self.buttonsurfaces[a].get_width()*scale,self.buttonsurfaces[a].get_height()*scale))
        surf = self.buttonsurfaces
        self.buttons = [[surf[0],'b',(self.x+self.backingsize[0]-16,self.y+16),'remove'],[surf[2],'b',(self.x+self.backingsize[0]/2,self.y+500),'team'],[surf[3],'b',(self.x+self.backingsize[0]/2,self.y+620),'character'],[surf[4],'b',(self.x+self.backingsize[0]/2,self.y+740),'ai'],[surf[5],'i',(self.x+self.backingsize[0]*0.05,self.y+120),'net']]
        if pm[1] == 1: del self.buttons[0]
        if pm[0]==(pm[1]-1) and pm[1]!=4:
            self.buttons.append([surf[1],'b',(self.x+self.backingsize[0]+56,self.y+16),'add'])
            
    def tick(self,screen,scale,mpos,mprs,mousedata):
        self.draw(screen,scale)
        r = 0
        for a in self.buttons:
            if a[1] == 'b':
                if button(a[0],a[2],mpos,mprs,mousedata,screen,scale):
                    if a[3] == 'remove': r = 1
                    elif a[3] == 'add': r = 2
                    elif a[3] == 'team':
                        self.team = (self.team+1)%len(self.teamcols)
                        self.idledude = PLAYER(self.x+self.backingsize[0]/2,self.y+200,[],self.team,self.teamcols,scale,self.character,[],[0,32],8,0,'',self.characterdic,1,1,1,1)
                    elif a[3] == 'character':
                        self.character = self.characterdic[(self.characterdic.index(self.character)+1)%len(self.characterdic)]
                        self.idledude = PLAYER(self.x+self.backingsize[0]/2,self.y+200,[],self.team,self.teamcols,scale,self.character,[],[0,32],8,0,'',self.characterdic,1,1,1,1)
                    elif a[3] == 'ai':
                        if self.aicontrolled: self.aicontrolled = False
                        else: self.aicontrolled = True
            elif a[1] == 'i':
                if a[3] == 'net' and self.aicontrolled:
                    screen.blit(a[0],(a[2][0]*scale,a[2][1]*scale))
                    
        return r
    def draw(self,screen,scale):
        screen.blit(self.backings[self.team],(self.x*scale,self.y*scale))
        write((self.x+self.backingsize[0]/2)*scale,(self.y+50)*scale,self.playername,(72,72,72),int(70*scale),screen,True)
        self.idledude.draw(screen,scale,False,[0,0])
        self.idledude.animate([],scale,[],0,[])

class MAP_EDITOR(MAP):
    def __init__(self,x,y,rw,rh,scale,mapid,displaybox):
        super().__init__(x,y,rw,rh,scale,-1)
        self.playerspawnlocdraw = True
        self.truedisplaybox = displaybox
        self.moveprevcords = [0,0]
        self.editvresetscale(scale)
        self.middleclickholding = False
        self.nclickholding = True
        self.mapeditpattern = [[0]]
        self.pattern = [[0]]
        self.selectedtile = 1
        self.tilehovering = -1
        self.mprs = [0,0,0]

        #x,y,rw,rh,pattern,block id
        self.bbdata = [[1653,53,100,100,[[1]],1],[1847,58,100,100,[[2]],2],[1653,216,100,100,[[3]],3],[1862,190,75,75,[[4],[0]],4],[1653,400,100,100,[['p1']],'p1'],[1847,400,100,100,[['p2']],'p2'],[1653,600,100,100,[['p3']],'p3'],[1862,600,100,100,[['p4']],'p4']] 
        self.blockbuttons = [MAP(a[0],a[1],a[2],a[3],scale,-1) for a in self.bbdata]
        for a in range(len(self.blockbuttons)):
            self.blockbuttons[a].playerspawnlocdraw = True
            self.blockbuttons[a].pattern = self.bbdata[a][4]
            self.blockbuttons[a].gridgen()

    def editvdraw(self,screen,scale,cam,debug):
        dispsurf = pygame.Surface((self.displaybox.width,self.displaybox.height))
        dispsurf.fill((79,173,245))
        self.draw(dispsurf,scale,cam)
        if debug:
            pygame.draw.circle(screen,(0,0,255),((self.x-cam[0])*scale,(self.y-cam[1])*scale),10)
            pygame.draw.circle(screen,(255,0,0),((self.truex-cam[0])*scale,(self.truey-cam[1])*scale),10)
            pygame.draw.rect(dispsurf,(100,100,100),(self.x*scale,self.y*scale,self.w*self.rw*scale,self.h*self.rh*scale),3)
        dispsurf.set_colorkey((79,173,245))
        screen.blit(dispsurf,(self.displaybox.x,self.displaybox.y))
        pygame.draw.rect(screen,(72,72,72),self.displaybox,4,10)
        for i,a in enumerate(self.blockbuttons):
            a.draw(screen,scale,cam)
            if i == self.selectedtile or i == self.tilehovering:
                inness = 0.25
                if i == self.selectedtile:
                    inness = 0.15
                    if self.mprs[0] and i == self.tilehovering: inness = 0.1
                if i == 3: extravert = 1
                else: extravert = 0
                if self.bbdata[i][5] in ['p1','p2','p3','p4']: vertup,extravert = 0.45,-0.1
                else: vertup = 0
                pygame.draw.rect(screen,(252,248,63),pygame.Rect((a.x-a.rw*inness)*scale,(a.y-vertup*a.rh-a.rh*inness)*scale,(a.w+inness*2)*a.rw*scale,(a.h+vertup+extravert+inness*2)*a.rh*scale),int(5*scale))
        
        
    def editvresetscale(self,scale):
        self.displaybox = pygame.Rect(self.truedisplaybox.x*scale,self.truedisplaybox.y*scale,self.truedisplaybox.width*scale,self.truedisplaybox.height*scale)
        self.resetscale(scale)
        
    def mousecontrol(self,mpos,mprs,scale):
        self.mprs = mprs
        if mprs[1] and not self.middleclickholding:
            self.moveprevcords = mpos[:]
            self.middleclickholding = True
        elif mprs[1]:
            self.truex-=(self.moveprevcords[0]-mpos[0])/scale
            self.truey-=(self.moveprevcords[1]-mpos[1])/scale
            for a in self.playerspawnlocplayers:
                a.x-=(self.moveprevcords[0]-mpos[0])/scale
                a.y-=(self.moveprevcords[1]-mpos[1])/scale
            self.moveprevcords = mpos[:]
        if mprs[0] and not self.nclickholding:
            if self.displaybox.collidepoint(mpos):
                clickcord = [((mpos[0]/scale)-self.displaybox.x-self.x)/self.rw,((mpos[1]/scale)-self.displaybox.y-self.y)/self.rh]
                if clickcord[0]<0: clickcord[0]-=1
                if clickcord[1]<0: clickcord[1]-=1
                clickcord = [int(clickcord[0]),int(clickcord[1])]
                self.mapeditpattern,clickcord = self.patternextend(self.mapeditpattern,clickcord)
                if self.bbdata[self.selectedtile][5] in ['p1','p2','p3','p4']:
                    for a in range(len(self.mapeditpattern)):
                        for b in range(len(self.mapeditpattern[a])):
                            if self.mapeditpattern[a][b] == self.bbdata[self.selectedtile][5]:
                                self.mapeditpattern[a][b] =  0
                self.mapeditpattern[clickcord[1]][clickcord[0]] = self.bbdata[self.selectedtile][5]
                self.mapeditpattern = self.patternlimit(self.mapeditpattern)
                self.pattern = copy.deepcopy(self.mapeditpattern)
                self.gridgen()
        if mprs[2] and self.displaybox.collidepoint(mpos):
            clickcord = [((mpos[0]/scale)-self.displaybox.x-self.x)/self.rw,((mpos[1]/scale)-self.displaybox.y-self.y)/self.rh]
            if clickcord[0]<0: clickcord[0]-=1
            if clickcord[1]<0: clickcord[1]-=1
            clickcord = [int(clickcord[0]),int(clickcord[1])]
            if clickcord[0]>-1 and clickcord[0]<len(self.mapeditpattern[0]) and clickcord[1]>-1 and clickcord[1]<len(self.mapeditpattern):
                self.mapeditpattern[clickcord[1]][clickcord[0]] = 0
                self.mapeditpattern = self.patternlimit(self.mapeditpattern)
                self.pattern = copy.deepcopy(self.mapeditpattern)
                self.gridgen()

        hov = False
        for i,a in enumerate(self.blockbuttons):
            if pygame.Rect(a.x*scale,a.y*scale,a.rw*scale,a.rh*scale).collidepoint(mpos):
                self.tilehovering = i
                hov = True
                if mprs[0] and not self.nclickholding:
                    self.nclickholding = True
                    self.selectedtile = i
        if not hov: self.tilehovering = -1

        if mprs[0] and not self.displaybox.collidepoint(mpos):
            self.nlickholding = True
        if not mprs[1]:
            self.middleclickholding = False
        if not(mprs[0] or mprs[2]):
            self.nclickholding = False
            

    def patternextend(self,pattern,cord):
        if cord[0]<0:
            for a in range(abs(cord[0])):
                for b in pattern:
                    b.insert(0,0)
                self.patterncenter[0]+=1
                self.w+=1
            cord[0] = 0
        elif cord[0]>len(pattern[0])-1:
            for a in range(cord[0]-len(pattern[0])+1):
                for b in pattern:
                    b.append(0)
                self.w+=1
        if cord[1]<0:
            for a in range(abs(cord[1])):
                pattern.insert(0,[0 for b in range(len(pattern[0]))])
                self.patterncenter[1]+=1
                self.h+=1
            cord[1] = 0
        elif cord[1]>len(pattern)-1:
            for a in range(cord[1]-len(pattern)+1):
                pattern.append([0 for b in range(len(pattern[0]))])
                self.h+=1
        return pattern,cord
    def patternlimit(self,pattern):
        horizempty = [0 for a in range(len(pattern[0]))]
        while pattern[0] == horizempty and len(pattern)>1:
            del pattern[0]
            self.patterncenter[1]-=1
            self.h-=1
        while pattern[-1] == horizempty and len(pattern)>1:
            del pattern[-1]
            self.h-=1
            
        vertempty = [0 for a in range(len(pattern))]
        while [pattern[a][0] for a in range(len(pattern))] == vertempty and len(pattern[0])>1:
            for a in pattern: del a[0]
            self.patterncenter[0]-=1
            self.w-=1
        while [pattern[a][-1] for a in range(len(pattern))] == vertempty and len(pattern[0])>1:
            for a in pattern: del a[-1]
            self.w-=1

        return pattern

    
            
        
        
            
                

class MAIN:
    done = False
    clock = pygame.time.Clock()
    debug = False
    display = 'menu'
    mousedata = [False,-1]
    #esc,enter
    keydata = [False,False]
    backbutton = []
    players = []
    teamcols = [(0,162,232),(237,28,36),(0,175,80),(163,73,164)]
    camera = [0,0]
    shakecamcords = [0,0]
    followcamcords = [0,0]
    camerashake = [0,0]
    scroll = 0
    selectededitmap = -1

    ais = [0,0,0,0]
    
    def __init__(self):
        self.loadsettings()
        self.screenwidth = 2000*self.screenscale
        self.screenheight = 1200*self.screenscale
        self.screen = pygame.display.set_mode((self.screenwidth,self.screenheight))
        self.map = 0
        self.wallpaper = WALLPAPER(self.screenscale)
        self.mapselect = 0
        self.mapprev = MAP(1014,1000,16,16,self.screenscale,self.mapselect)
        self.mapeditmap = MAP_EDITOR(720,400,80,80,self.screenscale,1,pygame.Rect(0,0,1600,960))
        self.maplistmaps = [MAP(0,0,20,20,self.screenscale,a) for a in range(len(self.mapeditmap.mappatterns))]
        self.maplistsorter()

        self.music = pygame.mixer.music.load('so_far.mp3')
        
        #num of images,image size, y of images from base, button or slider
        self.buttonsizes = [[3,[326,206],0,'b'],[3,[166,126],206,'b'],[3,[142,142],332,'b'],[3,[418,204],474,'b'],[3,[52,94],678,'s',0],[3,[340,150],772,'b'],[3,[340,150],922,'b'],[3,[418,202],1072,'b'],[3,[276,202],1274,'b'],[3,[476,212],1476,'b'],[3,[276,202],1688,'b'],[3,[96,52],1890,'s'],[3,[284,160],1942,'b'],[3,[260,150],2102,'b'],[3,[260,150],2252,'b'],[3,[320,134],2402,'b'],[3,[320,134],2536,'b'],[3,[320,134],2670,'b']]
        #num of images, image size, y of images from base,slider image size ,where slider sits on image, slider control
        self.sliderdata = [[1,[458,188],0,[26,70],[40,148,378,0],[0,2,self.screenscale]],[1,[458,188],188,[26,70],[40,148,378,0],[0,3,self.particleintensity]],[1,[458,188],376,[26,70],[40,148,378,0],[0,5,self.camerashakeintensity]],[1,[458,188],564,[26,70],[40,148,378,0],[0.1,1,self.cameraplayerfollow]],[1,[458,188],752,[74,26],[416,66,0,56],[1,0,self.particlephysicstoggle]],[1,[458,188],940,[26,70],[40,148,378,0],[0,1,self.musicvolume]]]

        #character    attacks:shape,radius/width,height,damage,kb,stunned,cords,impact,velocity,name,cooldown    hitbox    walkspeed   dashspeed   dashduration   health

        self.characterdic = ['ken','harry','alex']
        self.characters = [['ken',[[('circle',5,-1,20,30,10,(10,0),10,0,'punch',25),('rect',16,10,20,30,10,(2,0),10,0,'punch',25),('circle',5,-1,25,5,10,(10,0),15,20,'spell',25)],[('circle',15,-1,8,20,10,(0,0),20,0,'dash',30)],[('circle',24,-1,35,40,30,(0,0),50,0,'flip',35)]],[10,32],1.5,30,15,100],
                           ['harry',[[('circle',5,-1,55,10,20,(10,-10),30,20,'rock',50)],[('circle',15,-1,12,20,10,(0,0),30,0,'dash',30)],[('rect',25,30,78,40,45,(15,5),80,0,'smash',50)]],[16,40],0.8,20,20,180],
                           ['alex',[[('circle',10,-1,55,10,25,(20,-10),25,30,'stick',35)],[('circle',30,-1,25,25,15,(0,0),30,0,'dash',30)],[('circle',18,-1,65,35,30,(30,4),50,0,'sticksmash',35),('circle',8,-1,65,35,30,(45,15),50,0,'sticksmash',35)]],[8,34],1.3,20,30,125]]
        #dps
        #ken    10.4  4  20.4
        #harry  45.8  4  20.4
        self.playercreationtabs = [PLAYERCREATIONTAB(self.screenscale,a%4,self.teamcols,[a,2],a+1,self.characterdic,self.ais[a]) for a in range(3)]
        self.scaleset(self.screenscale)
        
    def scaleset(self,scale):
        self.screenscale = scale
        self.screenwidth = 2000*scale
        self.screenheight = 1200*scale
        self.screen = pygame.display.set_mode((self.screenwidth,self.screenheight))
        self.wallpaper.resetscale(self.screenscale)
        for a in range(len(self.playercreationtabs)): self.playercreationtabs[a].resetscalepos(self.screenscale,[a,len(self.playercreationtabs)])
        if self.map!=0:
            self.map.resetscale(self.screenscale)
            self.map.center(pygame.Rect(0,0,2000,1200))
        self.mapprev.resetscale(self.screenscale)
        self.mapeditmap.editvresetscale(self.screenscale)
        for a in self.maplistmaps: a.resetscale(self.screenscale)
        for a in self.players: a.resetscale(self.screenscale)
        
        self.buttonimg = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+'buttons.png')
        self.buttonimg = pygame.transform.scale(self.buttonimg,(self.buttonimg.get_width()*2,self.buttonimg.get_height()*2))
        self.sliderimg = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+'sliders.png')
        self.sliderimg = pygame.transform.scale(self.sliderimg,(self.sliderimg.get_width()*2,self.sliderimg.get_height()*2))
        self.pausemenu = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+'pause menu.png')
        self.pausemenu = pygame.transform.scale(self.pausemenu,(self.pausemenu.get_width()*3*self.screenscale,self.pausemenu.get_height()*3*self.screenscale))
        self.pausemenu.set_colorkey((255,255,255))
        
        self.buttonsurfaces = [pygame.Surface((a[1][0]*a[0],a[1][1])) for a in self.buttonsizes]
        for a in range(len(self.buttonsurfaces)):
            self.buttonsurfaces[a].blit(self.buttonimg,(0,0),(0,self.buttonsizes[a][2],self.buttonsizes[a][1][0]*self.buttonsizes[a][0],self.buttonsizes[a][1][1]))
            self.buttonsurfaces[a].set_colorkey((255,255,255))
            self.buttonsurfaces[a] = pygame.transform.scale(self.buttonsurfaces[a],(self.buttonsurfaces[a].get_width()*self.screenscale,self.buttonsurfaces[a].get_height()*self.screenscale))
        surf = self.buttonsurfaces
        self.sliders = []
        for a in range(len(self.sliderdata)):
            ts = pygame.Surface((self.sliderdata[a][1][0]*self.sliderdata[a][0],self.sliderdata[a][1][1]))
            ts.blit(self.sliderimg,(0,0),(0,self.sliderdata[a][2],self.sliderdata[a][1][0]*self.sliderdata[a][0],self.sliderdata[a][1][1]))
            ts.set_colorkey((255,255,255))
            ts = pygame.transform.scale(ts,(ts.get_width()*self.screenscale,ts.get_height()*self.screenscale))
            self.sliders.append([ts,self.sliderdata[a][3],self.sliderdata[a][4],self.sliderdata[a][5]])

        self.menudict = {'menu':0,'settings':1,'paused':2,'makegame':3,'mapeditor':4,'maplistsave':5,'maplistselect':6}
        self.menudata = [[[surf[0],'b',(1000,600),'makegame'],[surf[1],'b',(1900,1130),'quit'],[surf[2],'b',(100,1100),'settings'],[surf[12],'b',(1000,820),'mapeditor']],
                         [[surf[1],'b',(1900,1130),'quit'],[surf[4],'s',(750,300),'scale',self.sliders[0]],[surf[4],'s',(1250,300),'particles',self.sliders[1]],[surf[4],'s',(750,550),'shake',self.sliders[2]],[surf[4],'s',(1250,550),'follow',self.sliders[3]],[surf[11],'s',(750,800),'particlephysics',self.sliders[4]],[surf[4],'s',(1250,800),'musicvolume',self.sliders[5]],[surf[5],'b',(800,1050),'back'],[surf[6],'b',(1200,1050),'apply']],
                         [[surf[1],'b',(1220,930),'quit'],[surf[2],'b',(780,930),'settings'],[surf[3],'b',(1000,420),'resume'],[surf[7],'b',(1000,630),'menu'],[surf[8],'b',(1000,840),'game']],
                         [[surf[9],'b',(1730,1070),'game'],[surf[10],'b',(800,1090),'maplistselect'],[surf[2],'b',(100,1100),'settings'],[surf[5],'b',(400,1100),'back']],
                         [[surf[1],'b',(1900,1130),'quit'],[surf[2],'b',(100,1100),'settings'],[surf[5],'b',(400,1100),'back'],[surf[13],'b',(800,1100),'maplistsave']],
                         [[surf[1],'b',(1900,1130),'quit'],[surf[2],'b',(100,1100),'settings'],[surf[5],'b',(400,1100),'back'],[surf[14],'b',(700,1100),'loadmap'],[surf[15],'b',(1000,1100),'newsave'],[surf[16],'b',(1330,1100),'overwrite'],[surf[17],'b',(1650,1100),'deletemap']],
                         [[surf[1],'b',(1900,1130),'quit'],[surf[2],'b',(100,1100),'settings'],[surf[5],'b',(400,1100),'back']]]
        
    
    def gengame(self,randommap=False):
        self.camera = [0,0]
        charnum = 0
        self.playercreationtabs.sort(key = lambda x: x.playernum)

        spawnpos = [a for a in range(4)]
        if randommap:
            self.mapselect = random.randint(0,len(self.mapprev.mappatterns)-1)
            random.shuffle(spawnpos)
        
        self.map = MAP(0,0,100,100,self.screenscale,self.mapselect)
        self.map.center(pygame.Rect(0,0,2000,1200))
        spawncords = self.map.playercords
        #self.playerinfo = [[a.team] for a in self.playercreationtabs]
        
        self.playerdata = [[self.controls[a],
                            self.characters[self.characterdic.index(self.playercreationtabs[a].character)],
                            self.playercreationtabs[a].team,
                            [spawncords[spawnpos[a]][0]-self.characters[self.characterdic.index(self.playercreationtabs[a].character)][2][0]/2,spawncords[spawnpos[a]][1]-self.characters[self.characterdic.index(self.playercreationtabs[a].character)][2][1]*4],
                            self.playercreationtabs[a].playername,
                            self.playercreationtabs[a].character,
                            self.playercreationtabs[a].aicontrolled]
                           for a in range(len(self.playercreationtabs))]
        self.players = []
        usedids = [a.id for a in self.players]
        if usedids == []: usedids = [-1]
        for i,a in enumerate(self.playerdata):
            nid = max(usedids)+1
            usedids.append(nid)
            if a[6]:
                self.players.append(AIPOWEREDPLAYER(a[3][0],a[3][1],a[0],a[2],self.teamcols,self.screenscale,a[1][0],a[1][1],a[1][2],4,nid,a[4],self.characterdic,a[1][3],a[1][4],a[1][5],a[1][6]))
            else:
                self.players.append(PLAYER(a[3][0],a[3][1],a[0],a[2],self.teamcols,self.screenscale,a[1][0],a[1][1],a[1][2],4,nid,a[4],self.characterdic,a[1][3],a[1][4],a[1][5],a[1][6]))
            

        self.damages = []
        self.particles = []
        self.wintext = ''
        self.display = 'game'

        pygame.mixer.music.play(100)
        
    def gameloop(self):
        while not self.done:
            self.pyevent()
            self.wallpaper.draw(self.screen,self.display,self.screenscale)
            if self.display == 'game':
                self.gametick()
                self.drawgame()
            else:
                if self.display == 'paused':
                    self.drawgame()
            self.menutick()
            pygame.display.flip()
                
            self.clock.tick(60)
        pygame.quit()
        
    def pyevent(self):
        self.keydata = [False,False]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keydata[0] = True
                elif event.key == pygame.K_RETURN:
                    self.keydata[1] = True
                elif event.key == pygame.K_F3:
                    if self.debug: self.debug = False
                    else: self.debug = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: self.scroll-=50
                elif event.button == 5: self.scroll+=50
                if self.scroll<0: self.scroll = 0
                
    def drawgame(self):
        self.map.draw(self.screen,self.screenscale,self.camera)
        #pygame.display.flip()
        #pygame.image.save(self.screen,'map.png')
        for a in self.players:
            a.draw(self.screen,self.screenscale,self.debug,self.camera)
        if self.debug:
            for a in self.damages:
                a.draw(self.screen,self.screenscale,self.camera)
        for a in self.particles:
            a.draw(self.screen,self.screenscale,self.camera)
        for a in self.damages:
            if a.typ == 'spell' or a.typ == 'rock' or a.typ == 'stick':
                a.spelldraw(self.screen,self.screenscale,self.camera)
        if self.wintext != '': write(1000*self.screenscale,150*self.screenscale,self.wintext[0],self.wintext[1],int(100*self.screenscale),self.screen,True)
        for a in self.players:
            if a.aipowered and a.net.displayx<2000:
                a.net.displaynetwork(self.screen,[0,0,0,0])
        
    def gametick(self):
        for a in self.damages:
            self.particles,remove,self.camerashake = a.move(self.map,self.particles,self.particleintensity,self.camerashake)
            a.timer-=1
            if a.timer<0 or remove:
                self.damages.remove(a)
        self.camerashake[0]-=1
        if self.camerashake[0]>0:
            self.shakecamcords = [random.gauss(0,self.camerashake[1]*self.camerashakeintensity),random.gauss(0,self.camerashake[1]*self.camerashakeintensity)]
        else:
            self.camerashake[1] = 0
            self.shakecamcords = [0,0]
        self.camerafollow()
        self.camera = [int(self.followcamcords[0]+self.shakecamcords[0]),int(self.followcamcords[1]+self.shakecamcords[1])]
        for a in self.players:
            a.control(self.map,self.players,self.damages)
            self.damages = a.move(self.map,self.damages,self.screenscale)
            self.damages,self.particles,self.camerashake = a.animate(self.damages,self.screenscale,self.particles,self.particleintensity,self.camerashake)
            self.particles = a.checkdamage(self.damages,self.particles,self.particleintensity)
            if a.health<0 or a.y>self.map.y+self.map.h*self.map.rh+500:
                self.particles = a.death(self.particles,self.particleintensity)
                self.players.remove(a)
                teams = []
                if len(self.players) == 0:
                    self.wintext = ['DRAW',(150,150,150)]
                    self.gengame()
                else:
                    for b in self.players:
                        if (not (b.team in teams)) and len(self.players)>1 and len(teams)>0:
                            break
                        teams.append(b.team)
                    else:
                        if teams[0] == 0: self.wintext = ['BLUE WON',self.teamcols[teams[0]]]
                        elif teams[0] == 1: self.wintext = ['RED WON',self.teamcols[teams[0]]]
                        elif teams[0] == 2: self.wintext = ['GREEN WON',self.teamcols[teams[0]]]
                        elif teams[0] == 3: self.wintext = ['PURPLE WON',self.teamcols[teams[0]]]
                        else: ['SOMEONE WON I THINK',(0,0,0)]
        
        for a in self.particles:
            if a.move(self.map,self.particlephysicstoggle):
                self.particles.remove(a)
    def applysettings(self):
        for a in self.menudata[self.menudict.get(self.display)]:
            if a[1] == 's':
                if a[3] == 'scale':
                    self.scaleset(a[4][3][2])
                elif a[3] == 'particles':
                    self.particleintensity = a[4][3][2]
                elif a[3] == 'shake':
                    self.camerashakeintensity = a[4][3][2]
                elif a[3] == 'follow':
                    self.cameraplayerfollow = a[4][3][2]
                elif a[3] == 'particlephysics':
                    self.particlephysicstoggle = a[4][3][2]
                elif a[3] == 'musicvolume':
                    self.musicvolume = a[4][3][2]
                    pygame.mixer.music.set_volume(self.musicvolume)
                    
        self.savesettings()

    def mapeditortick(self,mpos,mprs):
        self.mapeditmap.editvdraw(self.screen,self.screenscale,[0,0],self.debug)
        self.mapeditmap.mousecontrol(mpos,mprs,self.screenscale)
    def menutick(self):
        mpos = pygame.mouse.get_pos()
        mprs = pygame.mouse.get_pressed()
            
        if self.display == 'paused': self.pausetick()
        elif self.display == 'makegame':
            self.mapprev.draw(self.screen,self.screenscale,[0,0])
            pygame.draw.rect(self.screen,(72,72,72),pygame.Rect((self.mapprev.truex-(self.mapprev.patterncenter[0])*self.mapprev.rw)*self.screenscale,(self.mapprev.truey-(self.mapprev.patterncenter[1])*self.mapprev.rh)*self.screenscale,self.mapprev.w*self.mapprev.rw*self.screenscale,self.mapprev.h*self.mapprev.rh*self.screenscale),int(3*self.screenscale)+1,int(4*self.screenscale))
            for a in self.playercreationtabs:
                t = a.tick(self.screen,self.screenscale,mpos,mprs,self.mousedata)
                if t == 1:
                    self.playercreationtabs.remove(a)
                    for b in range(len(self.playercreationtabs)): self.playercreationtabs[b].resetscalepos(self.screenscale,[b,len(self.playercreationtabs)])
                elif t == 2:
                    n = [b.playernum for b in self.playercreationtabs]
                    c = 1
                    while c in n: c+=1
                    self.playercreationtabs.append(PLAYERCREATIONTAB(self.screenscale,c-1,self.teamcols,[len(self.playercreationtabs),len(self.playercreationtabs)-1,self.playercreationtabs],c,self.characterdic,self.ais[len(self.playercreationtabs)]))
                    for b in range(len(self.playercreationtabs)): self.playercreationtabs[b].resetscalepos(self.screenscale,[b,len(self.playercreationtabs)])
        elif self.display == 'mapeditor': self.mapeditortick(mpos,mprs)
        elif 'maplist' in self.display: self.maplistdraw(mpos,mprs)


        if self.keydata[1]:
            if self.display == 'settings':
                self.applysettings()
        elif self.keydata[0]:
            if self.display == 'menu': self.done = True
            elif self.display == 'game':
                self.display = 'paused'
                pygame.mixer.music.pause()
            elif self.display == 'paused':
                self.display = 'game'
                pygame.mixer.music.unpause()
            elif self.display in ['settings','makegame','mapeditor','maplistsave','maplistload']:
                self.display = self.backbutton[-1]
                del self.backbutton[-1]

                
        if self.display in self.menudict:
            for c,a in enumerate(self.menudata[self.menudict.get(self.display)]):
                if a[1] == 'b':
                    if button(a[0],a[2],mpos,mprs,self.mousedata,self.screen,self.screenscale):
                        if a[3] == 'game': self.gengame()
                        elif a[3] == 'resume': self.display = 'game'
                        elif a[3] == 'quit': self.done = True
                        elif a[3] == 'back':
                            self.display = self.backbutton[-1]
                            del self.backbutton[-1]
##                        elif a[3] == 'mapsel':
##                            self.mapselect = (self.mapselect+1)%len(self.mapprev.mappatterns)
##                            self.mapprev.mapid = self.mapselect
##                            self.mapprev.regenpattern(self.screenscale)
                        elif a[3] == 'apply':
                            self.display = 'settings'
                            self.applysettings()
                        elif a[3] == 'newsave': self.savemaps(-1,False)
                        elif a[3] == 'overwrite': self.savemaps(self.selectededitmap,False)
                        elif a[3] == 'deletemap': self.savemaps(self.selectededitmap,True)
                        elif a[3] == 'loadmap': self.mapload(self.maplistmaps[self.selectededitmap])
                        else:
                            if a[3] in ['settings','makegame','mapeditor','maplistsave','maplistselect']:
                                self.backbutton.append(self.display)
                                self.mapeditmap.nclickholding = True
                            self.display = a[3]

                else:
                    t = slider(a[0],a[4],a[2],mpos,mprs,self.mousedata,self.screen,self.screenscale,c)
                    if t[0] == 1:
                        self.mousedata[1] = c
        if not(mprs[0]):
            self.mousedata = [False,-1]
        elif not(self.mousedata[0]):
            self.mousedata[0] = True
        write(1985*self.screenscale,15*self.screenscale,str(int(self.clock.get_fps())),(150,150,150),20*self.screenscale,self.screen,True)
    def maplistsorter(self):
        curx = 2
        cury = 2
        maxh = 0
        for a in self.maplistmaps:
            if curx+a.rw*(a.w+1)>2000:
                cury+=maxh
                maxh = 0
                curx = 2
            a.truex = (curx+a.rw/2)+a.patterncenter[0]*a.rw
            a.truey = (cury+a.rh/2)+a.patterncenter[1]*a.rh
            curx+=a.rw*(a.w+1)
            if maxh<a.rh*(a.h+1):
                maxh = a.rh*(a.h+1)
    def mapload(self,a):
        p = self.mapeditmap.patternlimit(copy.deepcopy(a.pattern))
        self.mapeditmap.mapeditpattern = p
        self.mapeditmap.pattern = p
        self.mapeditmap.center(pygame.Rect(0,0,1600,960))
        self.display = self.backbutton[-1]
        del self.backbutton[-1]
        self.mapeditmap.nclickholding = True
    def maplistdraw(self,mpos,mprs):
        dispsurf = pygame.Surface((2000*self.screenscale,960*self.screenscale))
        dispsurf.set_colorkey((0,0,0))
        for i,a in enumerate(self.maplistmaps):
            a.draw(dispsurf,self.screenscale,[0,self.scroll/self.screenscale])
            pygame.draw.rect(dispsurf,(72,72,72),pygame.Rect((a.x-a.rw/2)*self.screenscale,(a.y-a.rh/2)*self.screenscale-self.scroll,(a.w+1)*a.rw*self.screenscale,(a.h+1)*a.rh*self.screenscale),int(2*self.screenscale))
            if mpos[1]<960*self.screenscale and pygame.Rect((a.x-a.rw/2)*self.screenscale,(a.y-a.rh/2)*self.screenscale-self.scroll,(a.w+1)*a.rw*self.screenscale,(a.h+1)*a.rh*self.screenscale).collidepoint(mpos):
                if self.selectededitmap != i: inness = 0.3
                else: inness = 0.15
                if mprs[0]:
                    inness = 0
                    if 'save' in self.display:
                        self.selectededitmap = i
                    if 'select' in self.display:
                        self.mapselect = i
                        self.mapprev.mapid = self.mapselect
                        self.mapprev.regenpattern(self.screenscale)
                        self.display = self.backbutton[-1]
                        del self.backbutton[-1]
                pygame.draw.rect(dispsurf,(252,248,63),pygame.Rect((a.x-a.rw*inness)*self.screenscale,(a.y-a.rh*inness)*self.screenscale-self.scroll,(a.w+inness*2)*a.rw*self.screenscale,(a.h+inness*2)*a.rh*self.screenscale),int(5*self.screenscale))
            elif self.selectededitmap == i and 'save' in self.display:
                inness = 0.15
                pygame.draw.rect(dispsurf,(252,248,63),pygame.Rect((a.x-a.rw*inness)*self.screenscale,(a.y-a.rh*inness)*self.screenscale-self.scroll,(a.w+inness*2)*a.rw*self.screenscale,(a.h+inness*2)*a.rh*self.screenscale),int(5*self.screenscale))
        self.screen.blit(dispsurf,(0,0))
        pygame.draw.line(self.screen,(72,72,72),(0,960*self.screenscale),(2000*self.screenscale,960*self.screenscale),int(4*self.screenscale))
    def savemaps(self,overwrite,delete):
        if not (delete and overwrite == -1):
            npatterns = copy.deepcopy(self.mapeditmap.mappatterns)
            if overwrite == -1:
                npatterns.append(copy.deepcopy(self.mapeditmap.mapeditpattern))
            else:
                if delete: del npatterns[overwrite]
                else: npatterns[overwrite] = copy.deepcopy(self.mapeditmap.mapeditpattern)
            lines = ''
            for a in npatterns:
                lines+=';\n'
                for y in range(len(a)):
                    for x in range(len(a[y])):
                        lines+=str(a[y][x])
                        if x!=len(a[y])-1:
                            lines+=','
                    lines+='\n'
            with open('maps.txt','w') as f:
                f.write(lines)
            if self.map!=0: self.map.mappatterns = copy.deepcopy(npatterns)
            self.mapprev.mappatterns = copy.deepcopy(npatterns)
            self.mapprev.gridgen()
            self.mapeditmap.mappatterns = copy.deepcopy(npatterns)
            
            for a in self.maplistmaps:
                a.mappatterns = copy.deepcopy(npatterns)
            if overwrite == -1:
                self.maplistmaps.append(MAP(0,0,20,20,self.screenscale,len(self.maplistmaps)))
            else:
                if delete: del self.maplistmaps[overwrite]
                else: self.maplistmaps[overwrite] = MAP(0,0,20,20,self.screenscale,overwrite)
            self.maplistsorter()
            if delete:
                if self.selectededitmap>len(npatterns)-1:
                    self.selectededitmap= -1
                        
        
    def camerafollow(self):
        scc = [1000,600]
        camfol = math.log10(self.cameraplayerfollow*10) 
        pnormal = []
        for a in self.players:
            if a.x-scc[0]>0: xmul = 1
            else: xmul = -1
            if a.y-scc[1]>0: ymul = 1
            else: ymul = -1
            xoff = ((abs(a.x-scc[0]))**camfol)*xmul+scc[0]-xmul
            yoff = ((abs(a.y-scc[1]))**camfol)*ymul+scc[1]-ymul
            pnormal.append([xoff,yoff])
        pcenter = [sum([a[0] for a in pnormal])/len(pnormal),sum([a[1] for a in pnormal])/len(pnormal)]
        #pcenter = [statistics.geometric_mean([a.x for a in self.players]),statistics.geometric_mean([a.y for a in self.players])]
        #pcenter = [sum([a.x for a in self.players])/len(self.players),sum([a.y for a in self.players])/len(self.players)]
        targetcords = [pcenter[0]-scc[0],pcenter[1]-scc[1]]#[pcenter[0]*(1-self.cameracenterweight)+scc[0]*self.cameracenterweight-scc[0],pcenter[1]*(1-self.cameracenterweight)+scc[1]*self.cameracenterweight-scc[1]]
        camspeed = 0.1
        self.followcamcords = [self.followcamcords[0]-(self.followcamcords[0]-targetcords[0])*camspeed,self.followcamcords[1]-(self.followcamcords[1]-targetcords[1])*camspeed]
        
    def pausetick(self):
        self.screen.blit(self.pausemenu,(1000*self.screenscale-self.pausemenu.get_width()/2,600*self.screenscale-self.pausemenu.get_height()/2))
    def savesettings(self):
        tx = 'screenscale: '+str(self.screenscale)+' \nparticles: '+str(self.particleintensity)+' \ncamerashake: '+str(self.camerashakeintensity)+' \ncamerafollow: '+str(self.cameraplayerfollow)+' \nparticlephysics: '+str(self.particlephysicstoggle)+' \nmusicvolume: '+str(self.musicvolume)+' \nplayer1controls: w s a d SPACE e q \nplayer2controls: UP DOWN LEFT RIGHT RETURN n m \nplayer3controls: t g f h 8 9 0 \nplayer4controls: i k j l b o p'
        with open('settings.txt','w') as f:
            f.write(tx)
    def loadsettings(self):
        try:
            with open('settings.txt','r') as f:
                lines = f.readlines()
        except:
            [[[pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d,pygame.K_SPACE,pygame.K_e,pygame.K_q],'ken'],
                           [[pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_RETURN,pygame.K_n,pygame.K_m],'ken'],
                           [[pygame.K_t,pygame.K_g,pygame.K_f,pygame.K_h,pygame.K_8,pygame.K_9,pygame.K_0],'ken'],
                           [[pygame.K_i,pygame.K_k,pygame.K_j,pygame.K_l,pygame.K_b,pygame.K_o,pygame.K_p],'ken']]
            
            linemake = 'screenscale: 1.0 \nparticles: 1.0 \ncamerashake: 1.0 \ncamerafollow: 1.0 \nparticlephysics: 1 \nmusicvolume: 1.0 \nplayer1controls: w s a d SPACE e q \nplayer2controls: UP DOWN LEFT RIGHT RETURN n m \nplayer3controls: t g f h 8 9 0 \nplayer4controls: i k j l b o p'
            with open('settings.txt','w') as f:
                f.write(linemake)
            with open('settings.txt','r') as f:
                lines = f.readlines()
        data = [a.split() for a in lines]
        for a in data:
            if 'screenscale' in a[0]: 
                self.screenscale = float(a[1])
            elif 'particles' in a[0]:
                self.particleintensity = float(a[1])
            elif 'camerashake' in a[0]:
                self.camerashakeintensity = float(a[1])
            elif 'camerafollow' in a[0]:
                self.cameraplayerfollow = float(a[1])
            elif 'particlephysics' in a[0]:
                self.particlephysicstoggle = int(a[1])
            elif 'musicvolume' in a[0]:
                self.musicvolume = float(a[1])
                pygame.mixer.music.set_volume(self.musicvolume)
        self.controls = [[pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d,pygame.K_SPACE,pygame.K_e,pygame.K_q],
                         [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_RETURN,pygame.K_n,pygame.K_m],
                         [pygame.K_t,pygame.K_g,pygame.K_f,pygame.K_h,pygame.K_8,pygame.K_y,pygame.K_r],
                         [pygame.K_i,pygame.K_k,pygame.K_j,pygame.K_l,pygame.K_0,pygame.K_o,pygame.K_u]]##        self.controls = [[pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d,pygame.K_SPACE,pygame.K_e,pygame.K_q],
##                         [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_RETURN,pygame.K_n,pygame.K_m],
##                         [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_RETURN,pygame.K_n,pygame.K_m],
##                         [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_RETURN,pygame.K_n,pygame.K_m]]
            

main = MAIN()
main.gameloop()
##pygame.mixer.
