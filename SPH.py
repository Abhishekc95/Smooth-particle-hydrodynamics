
import random
import pygame
import quadtree as qtr
import math as ma
import numpy as np


    
pygame.init()


width  = 500
height = 500

clock = pygame.time.Clock()
window = pygame.display.set_mode((width,height))
blue = (0,0,255)
red = (255,0,0)
green = (0,128,0)



g  = np.array([0,12000*9.8],dtype=float)  # gravity
ini_dens  = 1000                    # initial density
gas_const = 2000                    # gas constant
k = 10                              # kernal radius
ksq = k*k                           # kernal radius^2
mass = 65                           # mass of each fluid particle
nu = 250                            # viscosity
dt = 0.0008                         # time step for integration
wf = 315/(64*ma.pi*pow(k,9))      # weighing function
grad_wf = -45/(ma.pi*pow(k,6))    # weighing function for gradient
lap_wf = 45/(ma.pi*pow(k,6))      # weighing function for laplacian
damp = -0.5                         # for damping particle velocity as it interacts with boundary
 

class Particle:
    def __init__(self,r,xp,yp):
         self.xp = xp
         self.yp = yp
         self.pos = np.array([self.xp,self.yp],dtype=float)
         self.v   = np.array([0,0],dtype=float)
         self.f   = np.array([0,0],dtype=float)
         self.r   = r    
         self.p   = 0.0
         self.rho = 1.0
         #self.highlight = False
    
    def display(self,win):
        pygame.draw.circle(win,red,(int(self.pos[0]),int(self.pos[1])),self.r)
    


def eval_pressure_density(pi,sqt):

    for i in pi:
        ci = qtr.circle(i.pos[0],i.pos[1],k)
        f = []
        pj = sqt.nns(ci,f)
        for j in pj:
            rij = i.pos-j.pos
            rsq = (np.linalg.norm(rij))**2
            i.rho += mass*wf*pow(ksq-rsq,3)
        i.p = gas_const*(i.rho - ini_dens)            
    

def eval_force(pi,sqt):

    for i in pi:
        fpres = np.array([0,0],dtype=float)
        fvisc = np.array([0,0],dtype=float)
        ci = qtr.circle(i.pos[0],i.pos[1],k)
        f = []
        pj = sqt.nns(ci,f)
        for j in pj:
            if (j != i) :
                rij = i.pos-j.pos
                rd = np.linalg.norm(rij)    
                rn = rij/rd
                fpres +=  -mass*(i.p/i.rho**2 + j.p/j.rho**2)*grad_wf*pow(k-rd,2)*(rn)
                fvisc +=   nu *mass *((j.v - i.v)/j.rho)*lap_wf*(k-rd)
        fgrav = g*i.rho
        i.f = fpres + fvisc + fgrav
       
        for j in pj:
            if (j != i) :
                rij = i.pos-j.pos
                rsd = np.linalg.norm(rij)**2 
                v1,v2 = i.v,j.v
                u1 = v1 -((np.dot(v1-v2,i.pos-j.pos)/rsd)*(i.pos-j.pos))
                u2 = v2 -((np.dot(v2-v1,j.pos-i.pos)/rsd)*(j.pos-i.pos))
                i.v = u1
                j.v = u2
        
        i.v += dt*i.f/i.rho     
        i.pos += dt*i.v
          
        if (i.pos[0]-k < 0):
            i.v[0]*=damp
            i.pos[0] = k
        
        if (i.pos[0]+k > width):
            i.v[0]*=damp
            i.pos[0] = width-k
        
        if (i.pos[1]-k < 0):
            i.v[1]*=damp
            i.pos[1] = k

        if (i.pos[1]+k > height):
            i.v[1]*=damp
            i.pos[1] = height-k



    
    
t = True
p = [] 
r1 = qtr.rectangle(250,250,500,500)


for i in range(5,width//4,10):
    for j in range(height//2,height-150,10):
        p.append(Particle(5,i,j))
    

    

while t :
   
    
    qt1 = qtr.quadTree(r1,4)

    for i in p:
        qt1.insert(i)
        i.display(window)
    
    eval_pressure_density(p,qt1)
    eval_force(p,qt1)
    

    #qt1.display(window)
    
    pygame.display.update() 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            t = False
    
    window.fill((255,255,255))
       
    
    del qt1  
    
pygame.quit()



