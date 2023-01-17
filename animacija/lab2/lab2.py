import numpy as np
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import pygame
from pygame.locals import *
import random
from PIL import Image

#constants
INIT_PARTICLE_SIZE = 2
MAX_LIFE_SPAN = 7
SPEED = 7
SIZE_MULTIPLIER = 3
TEXTURE = "./cestica.bmp"

class Particle:
    def __init__(self):
        self.position = [0.0, -50.0, 0.0]
        self.age = 0
        self.size = INIT_PARTICLE_SIZE
        self.color = [0.0, 0.0, 0.0, 0.0]
        self.lifeSpan = random.randint(1, MAX_LIFE_SPAN)

    def increaseAge(self, increment = 1):
        self.age = self.age + increment
            
    def updateParams(self):
        offset_vector = np.array([round(random.uniform(-3, 3), 2), round(random.uniform(2, 6), 2), 0])
        t = (self.lifeSpan - self.age) / self.lifeSpan
       
        self.position = self.position + offset_vector*SPEED
        self.size = (self.size)*SIZE_MULTIPLIER
        self.updateColor(t)

    def updateColor(self, t):
        self.color[0] = t*9
        self.color[1] = t*5
        self.color[2] = t
        self.color[3] = t

class Source:
    def __init__(self):
        self.particles = []
    
    def createParticles(self, numberOfParticles = 3):
        for i in range(numberOfParticles):
            self.particles.append(Particle())

    def increaseParticleAge(self):
        list2 = []
        for particle in self.particles:
            particle.increaseAge()
            if particle.age < particle.lifeSpan:
                list2.append(particle)
        self.particles = list2

    def updateParticleParams(self):
        for particle in self.particles:
            particle.updateParams()  
        	

def drawParticles(particles):
    glPushMatrix()
    glBegin(GL_QUADS)

    for p in particles:
        
        glColor4d(*(p.color))
        
        glTexCoord2d(0, 0)
        glVertex3f(p.position[0] - p.size, p.position[1] - p.size, p.position[2])

        glTexCoord2d(1, 0)
        glVertex3f(p.position[0] + p.size, p.position[1] - p.size, p.position[2])

        glTexCoord2d(1, 1)
        glVertex3f(p.position[0] + p.size, p.position[1] + p.size, p.position[2])

        glTexCoord2d(0, 1)
        glVertex3f(p.position[0] - p.size, p.position[1] + p.size, p.position[2])

    glEnd()
    glPopMatrix()

def loadTexture():
    w, h = 256, 256
    particle = Image.open(TEXTURE)
    particle = np.array(list(particle.getdata()), np.uint8)
    texture = glGenTextures(1)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 1, w, h, GL_RGB, GL_UNSIGNED_BYTE, particle)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE)
    glEnable(GL_BLEND)
    glEnable(GL_TEXTURE_2D)
    return texture

def main():

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)    
    gluPerspective(45, (display[0]/display[1]), 0.1, 700)
    glTranslatef(0, 0, -200)
    loadTexture()
    source = Source()

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)


        source.createParticles()
        source.updateParticleParams()
        drawParticles(source.particles)
        source.increaseParticleAge()


        pygame.display.flip()
        pygame.time.wait(100)

main()