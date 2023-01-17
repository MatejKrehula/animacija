import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import pygame
from pygame.locals import *


OBJ_FILE = "teatreadar.obj"
CONTROL_POINTS = "controlPoints.txt"
SCALE = 1

MATRIX_B = np.array(
                    [[-1, 3,-3, 1],
                    [3, -6, 3, 0],
                    [-3, 0, 3, 0],
                    [1, 4, 1, 0]]
                   )


MATRIX_B_TICK = np.array(
                     [[-1, 3, -3, 1],
                     [2, -4, 2, 0],
                     [-1, 0, 1, 0]]
                    )

def readData():
    vertices= []
    faces = []

    file = open(OBJ_FILE, "r")
    for line in file:
        if line[0] == "v":
           vertex = line.split()
           vertices.append((float(vertex[1]), float(vertex[2]), float(vertex[3])))
        elif line[0] == "f": 
           face = line.split()
           faces.append((int(face[1]), int(face[2]), int(face[3])))     
    return (vertices, faces)


def readControlPoints():
    controlPoints = []
    file = open(CONTROL_POINTS, "r")
    for line in file:
        line = line.split()
        controlPoints.append((line[0], line[1], line[2]))
    
    return controlPoints


def calculateObjectPath(t, firstNPoints):
    tArray = (np.array([t**3, t**2, t, 1]) * 1/6).reshape(1, 4)
    tb = np.matmul(tArray, MATRIX_B)
    matrix_r = np.array(firstNPoints, dtype=float)
    final = np.matmul(tb, matrix_r)

    return final


def calculateFinalOrientation(t, firstNPoints):
    print(t)
    tArray = (np.array([t**2, t, 1]) * 1/2).reshape(1, 3)
    tbTick = np.matmul(tArray, MATRIX_B_TICK)
    matrix_r = np.array(firstNPoints, dtype=float)
    final = np.matmul(tbTick, matrix_r)

    return final

#pocetna i ciljna orijentaija 
#pocetna je ona gdje je orijentiran nas oblik, a ciljna je tangenta na nasu b spline krivulju
def calculateVectorAxis(s, e):
    i = s[1]*e[0][2] - e[0][1]*s[2]
    j = -(s[0]*e[0][2] - e[0][0]*s[2])
    k = s[0]*e[0][1] - s[1]*e[0][0]

    return np.array([i, j , k])


def calculateDegree(s, e):
    scalarProduct =  np.dot(s, e[0]) 
    multiply =  np.linalg.norm(s, 2) * np.linalg.norm(e[0], 2)
    cosine = scalarProduct / multiply

    return math.acos(cosine) * (180.0 / math.pi)



def calculateAnimationParams(controlsPoints):
    finalOrientation = []
    objectPath = []
    #os oko koje rotiramo nas oblik za 
    vectorAxis = []
    rotationalDegrees = []

    #racunamo po segmentima krivulje sve ove stvari
    while len(controlsPoints) >= 4:

        firstNPoints = controlsPoints[:4]
        controlsPoints.pop(0)

        t, step = 0, 0.05

        s = np.array([0, 0, 1])

        while t < 1:
            path = calculateObjectPath(t, firstNPoints)
            objectPath.append(path)
            e = calculateFinalOrientation(t, firstNPoints)
            finalOrientation.append(e)
            vectorAxis.append(calculateVectorAxis(s, e))
            rotationalDegrees.append(calculateDegree(s, e))

            t = t + step
            #s je smjer gdje je okrenuto
            s = e + path

            s = s[0]


    return finalOrientation, objectPath, vectorAxis, rotationalDegrees    


def drawPath(objectPath):
    glPushMatrix()
    glBegin(GL_LINES)
    glColor3fv((1, 0, 0))

    for i in range(len(objectPath) - 1):
        v1 = objectPath[i][0]
        v2 = objectPath[i + 1][0]
        glVertex3fv((v1[0], v1[1], v1[2]))
        glVertex3fv((v2[0], v2[1], v2[2]))

    glEnd()
    glPopMatrix()


def drawTangent(pathPoint, orientation):

    glPushMatrix()
    glColor3fv((1, 0.5, 0))
    glBegin(GL_LINES)

    spiralPoint = pathPoint[0]
    orient = orientation[0]

    glVertex3fv((spiralPoint[0], spiralPoint[1], spiralPoint[2]))
    glVertex3fv(tuple(map(lambda i, j: i + j, (spiralPoint[0], spiralPoint[1], spiralPoint[2]), (orient[0], orient[1], orient[2])*SCALE)) )

    glEnd()
    glPopMatrix()


def drawObject(pathPoint, degree, axis, vertices, faces):

    glPushMatrix()
    glTranslatef(pathPoint[0], pathPoint[1], pathPoint[2])
    glRotatef(degree, axis[0], axis[1], axis[2])
    glColor3fv((0, 0, 1))
    glBegin(GL_TRIANGLES)

    for face in faces:
        glVertex3fv(vertices[face[0] -1])
        glVertex3fv(vertices[face[1] -1])
        glVertex3fv(vertices[face[2] -1])
    glEnd()

    glPopMatrix()


def main():

    vertices, faces = readData()
    controlPoints = readControlPoints()
    finalOrientation, objectPath, vectorAxis, rotationalDegrees = calculateAnimationParams(controlPoints)
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)    
    gluPerspective(45, (display[0]/display[1]), 0.1, 700)
    glTranslatef(0, 0, -80)
    i = 0 
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        drawPath(objectPath)
        drawTangent(objectPath[i], finalOrientation[i])
        drawObject(objectPath[i][0], rotationalDegrees[i], vectorAxis[i], vertices, faces)
        pygame.display.flip()
        pygame.time.wait(20)

        if i == len(objectPath) -1:
            i = 0
        else:    
            i = i + 1 

main()
