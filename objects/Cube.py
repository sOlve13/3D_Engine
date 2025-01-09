import numpy as np
from objects.GameObject import *
import glm


class Cube(OpenGLObject):
    def __init__(self, vertex_shader_source, fragment_shader_source):
        
        self.trans = glm.mat4(1.0)
        
        self.vertices = np.array([
            [-0.5, -0.5, -0.5],  
            [ 0.5, -0.5, -0.5],  
            [ 0.5,  0.5, -0.5],  
            [-0.5,  0.5, -0.5],  
            [-0.5, -0.5,  0.5],  
            [ 0.5, -0.5,  0.5],  
            [ 0.5,  0.5,  0.5],  
            [-0.5,  0.5,  0.5],  
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 2, 2, 3, 0,  
            4, 5, 6, 6, 7, 4,  
            0, 4, 7, 7, 3, 0,  
            1, 5, 6, 6, 2, 1,  
            3, 2, 6, 6, 7, 3,  
            0, 1, 5, 5, 4, 0   
        ], dtype=np.uint32)

        self.colors = np.array([
            [1.0, 0.0, 0.0],  
            [0.0, 1.0, 0.0],  
            [0.0, 0.0, 1.0],  
            [1.0, 1.0, 0.0],  
            [1.0, 0.0, 1.0],  
            [0.0, 1.0, 1.0],  
            [1.0, 1.0, 1.0],  
            [0.0, 0.0, 0.0],  
        ], dtype=np.float32)

        self.normals = np.array([
            [ 0.0,  0.0, -1.0],  
            [ 0.0,  0.0,  1.0],  
            [-1.0,  0.0,  0.0],  
            [ 1.0,  0.0,  0.0],  
            [ 0.0,  1.0,  0.0],  
            [ 0.0, -1.0,  0.0],  
        ], dtype=np.float32)

        #vec = glm.vec4(1.0, 0.0, 0.0, 1.0)
        #trans = glm.mat4(1.0)
        #trans = glm.translate(trans, glm.vec3(1.0, 1.0, 0.0))
        #vec = trans * vec
        #print(vec)
        
        super().__init__(self.vertices, vertex_shader_source, fragment_shader_source)
        self.shader_program = super()._create_shader_program()

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def _setup_buffers(self):
        super()._setup_buffers()

        self.CBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.CBO)
        glBufferData(GL_ARRAY_BUFFER, self.colors.nbytes, self.colors, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self, MVP_H):
        glUseProgram(self.shader_program)
        MVP = MVP_H * self.trans 
        
        #transformLoc = glGetUniformLocation(self.shader_program, "transform")
        #glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(self.trans))
        
        mvp_loc = glGetUniformLocation(self.shader_program, "MVP")
        glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, glm.value_ptr(MVP))

            
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

        glBindVertexArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def __del__(self):
        glDeleteBuffers(1, [self.VBO])
        glDeleteBuffers(1, [self.EBO])
        glDeleteBuffers(1, [self.CBO])
        glDeleteVertexArrays(1, [self.VAO])
    
    def scale(self, scale):
        scale_matrix = glm.scale(glm.mat4(1.0), glm.vec3(scale, scale, scale))
        self.trans *= scale_matrix
        
    def rotate(self, angle_x, angle_y, angle_z):
        self.trans = glm.rotate(self.trans, glm.radians(angle_x), glm.vec3(1.0, 0.0, 0.0))  
        self.trans = glm.rotate(self.trans, glm.radians(angle_y), glm.vec3(0.0, 1.0, 0.0)) 
        self.trans = glm.rotate(self.trans, glm.radians(angle_z), glm.vec3(0.0, 0.0, 1.0))  
        
    def translate(self, x, y):
        self.trans = glm.translate(self.trans, glm.vec3(x, y, 0))