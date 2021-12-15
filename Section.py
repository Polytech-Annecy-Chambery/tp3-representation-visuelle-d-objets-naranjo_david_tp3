# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul
"""
import OpenGL.GL as gl

class Section:
    # Constructor
    def __init__(self, parameters = {}) :
        # Parameters
        # position: position of the wall 
        # width: width of the wall - mandatory
        # height: height of the wall - mandatory
        # thickness: thickness of the wall
        # color: color of the wall        

        # Sets the parameters
        self.vertices = []
        self.faces = []
        self.parameters = parameters
        
        # Sets the default parameters
        if 'position' not in self.parameters:
            self.parameters['position'] = [0, 0, 0]        
        if 'width' not in self.parameters:
            raise Exception('Parameter "width" required.')   
        if 'height' not in self.parameters:
            raise Exception('Parameter "height" required.')   
        if 'orientation' not in self.parameters:
            self.parameters['orientation'] = 0
        if 'thickness' not in self.parameters:
            self.parameters['thickness'] = 0.2    
        if 'color' not in self.parameters:
            self.parameters['color'] = [0.5, 0.5, 0.5]       
        if 'edges' not in self.parameters:
            self.parameters['edges'] = False             
            
        # Objects list
        self.objects = []

        # Generates the wall from parameters
        self.generate()   
        
    # Getter
    def getParameter(self, parameterKey):
        return self.parameters[parameterKey]
    
    # Setter
    def setParameter(self, parameterKey, parameterValue):
        self.parameters[parameterKey] = parameterValue
        return self     

    # Defines the vertices and faces 
    def generate(self):
        self.vertices = [
            [0, 0, 0],
            [0, 0, self.parameters['height']],
            [self.parameters['width'], 0, self.parameters['height']],
            [self.parameters['width'], 0, 0],
            [0, self.parameters['thickness'], 0],
            [0, self.parameters['thickness'], self.parameters['height']],
            [self.parameters['width'], self.parameters['thickness'], self.parameters['height']],
            [self.parameters['width'], self.parameters['thickness'], 0],
                ]
        self.faces = [
            [0, 3, 2, 1],
            [4, 7, 6, 5],
            [0, 4, 5, 1],
            [2, 3, 7, 6],
            [0, 3, 7, 4],
            [1, 2, 6, 5]
                ]   

    # Checks if the opening can be created for the object x
    def canCreateOpening(self, x):
        return self.parameters['position'][0] <= x.parameters['position'][0] \
            and self.parameters['position'][1] <= x.parameters['position'][1] \
            and self.parameters['position'][2] <= x.parameters['position'][2] \
            and self.parameters['position'][0] + self.parameters['width'] >= x.parameters['position'][0] + x.parameters['width'] \
            and self.parameters['position'][1] + self.parameters['thickness'] >= x.parameters['position'][1] + x.parameters['thickness'] \
            and self.parameters['position'][2] + self.parameters['height'] >= x.parameters['position'][2] + x.parameters['height']


    # Creates the new sections for the object x
    def createNewSections(self, x):
        objects = []
        firstOffset = x.parameters['position'][0] - self.parameters['position'][0]
        if firstOffset > 0:
            objects.append(Section({'position': self.parameters['position'], 'test': 'b', 'width': firstOffset, 'height': self.parameters['height']}))

        if x.parameters['position'][2] + x.parameters['height'] < self.parameters['position'][2] + self.parameters['height']:
            objects.append(Section({'position': [firstOffset + self.parameters['position'][0], self.parameters['position'][1], x.parameters['position'][2] + x.parameters['height']], 'width': x.parameters['width'], 'height': self.parameters['height'] - (x.parameters['position'][2] + x.parameters['height'])}))

        if x.parameters['position'][2] > self.parameters['position'][2]:
            objects.append(Section({'position': [firstOffset + self.parameters['position'][0], self.parameters['position'][1], self.parameters['position'][2]], 'width': x.parameters['width'], 'height': x.parameters['position'][2] - self.parameters['position'][2]}))

        lastOffset = (x.parameters['position'][0] + x.parameters['width'])
        if lastOffset < self.parameters['position'][0] + self.parameters['width']:
            objects.append(Section({'position': [x.parameters['position'][0] + x.parameters['width'], self.parameters['position'][1], self.parameters['position'][2]], 'width': self.parameters['position'][0] + self.parameters['width'] - lastOffset, 'height': self.parameters['height']}))
        return objects
        
    # Draws the edges
    def drawEdges(self):
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_LINE)
        gl.glPushMatrix()
        gl.glTranslatef(self.parameters['position'][0], self.parameters['position'][1], self.parameters['position'][2])
        gl.glRotatef(self.parameters['orientation'], 1, 0, 0)
        for face in self.faces:
            for i in range(len(face)):
                gl.glBegin(gl.GL_LINES)
                gl.glColor3fv([0.5 * 0.8, 0.5 * 0.8, 0.5 * 0.8])
                gl.glVertex3fv(self.vertices[face[i]], 0, 0)
                gl.glVertex3fv(self.vertices[face[(i + 1) % len(face)]], 0, 0)
                gl.glEnd()
        gl.glPopMatrix()
                    
    # Draws the faces
    def draw(self):
        if self.parameters['edges']:
            self.drawEdges()
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL) # on trace les faces : GL_FILL
        gl.glPushMatrix()
        gl.glTranslatef(self.parameters['position'][0], self.parameters['position'][1], self.parameters['position'][2])
        gl.glRotatef(self.parameters['orientation'], 1, 0, 0)
        for face in self.faces:
            gl.glBegin(gl.GL_QUADS) # Tracé d’un quadrilatère
            gl.glColor3fv(self.parameters['color'])

            for vertice in face:
                gl.glVertex3fv(self.vertices[vertice], 0, 0)
            gl.glEnd()
        gl.glPopMatrix()

  