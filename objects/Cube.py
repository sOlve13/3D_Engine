import numpy as np
from objects.GameObject import *
import glm


class Cube(OpenGLObject):
    def __init__(self, vertex_shader_source, fragment_shader_source):
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

        vec = glm.vec4(1.0, 0.0, 0.0, 1.0)
        trans = glm.mat4(1.0)
        trans = glm.translate(trans, glm.vec3(1.0, 1.0, 0.0))
        vec = trans * vec
        print(vec)
        
        super().__init__(self.vertices, vertex_shader_source, fragment_shader_source)

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

    def draw(self):
        glUseProgram(self.shader_program)

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
