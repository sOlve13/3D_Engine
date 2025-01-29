import numpy as np
from objects.GameObject import *
import glm
from objects.BitmapHandler import BitmapHandler
import ctypes
import math

"""
A class for rendering a textured sphere in OpenGL.

Creates a sphere mesh with texture coordinates and normal vectors.

Attributes:
    radius (float): Radius of the sphere
    sectors (int): Number of horizontal divisions
    stacks (int): Number of vertical divisions
    trans (glm.mat4): Transformation matrix
    vertices (numpy.ndarray): Vertex data including positions, normals and texture coords
    indices (numpy.ndarray): Index data for triangle faces
    texture (int): OpenGL texture ID
    
Methods:
    draw(projection_matrix, view, camera_position, light_pos): Renders the textured sphere
"""

class TexturedSphere(OpenGLObject):
    def __init__(self, vertex_shader_source, fragment_shader_source, texture_path, radius=1.0, sectors=32, stacks=16):
        self.radius = radius
        self.sectors = sectors
        self.stacks = stacks
        self.trans = glm.mat4(1.0)

        vertices = []
        indices = []

        for i in range(stacks + 1):
            V = i / stacks
            phi = V * math.pi
            
            for j in range(sectors + 1):
                U = j / sectors
                theta = U * 2 * math.pi
                
                x = math.cos(theta) * math.sin(phi)
                y = math.cos(phi)
                z = math.sin(theta) * math.sin(phi)
                
                nx = x
                ny = y
                nz = z
                
                u = U
                v = V
                
                vertices.extend([
                    self.radius * x, self.radius * y, self.radius * z,
                    nx, ny, nz,
                    u, v
                ])

        for i in range(stacks):
            for j in range(sectors):
                first = (i * (sectors + 1)) + j
                second = first + sectors + 1
                
                indices.extend([first, second, first + 1])
                indices.extend([second, second + 1, first + 1])

        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)

        super().__init__(self.vertices, vertex_shader_source, fragment_shader_source)

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        self.bitmap_handler = BitmapHandler()
        self.texture = self.bitmap_handler.load_texture(texture_path)

    def _setup_buffers(self):
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(6 * sizeof(GLfloat)))
        glEnableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self, projection_matrix, view, camera_position, light_pos):
        glUseProgram(self.shader_program)
        self.bitmap_handler.bind_texture(self.texture, GL_TEXTURE0)
        glUniform1i(glGetUniformLocation(self.shader_program, "texture1"), 0)
        light_pos = [1.2, 1.0, 2.0]
        light_color = [1.0, 1.0, 1.0]
        view_pos = [0.0, 0.0, 3.0]
        glUniform3f(glGetUniformLocation(self.shader_program, "lightPos"), *light_pos)
        glUniform3f(glGetUniformLocation(self.shader_program, "lightColor"), *light_color)
        glUniform3f(glGetUniformLocation(self.shader_program, "viewPos"), *view_pos)
        MVP = projection_matrix * view * self.trans
        mvp_location = glGetUniformLocation(self.shader_program, "MVP")
        model_location = glGetUniformLocation(self.shader_program, "model")
        glUniformMatrix4fv(mvp_location, 1, GL_FALSE, glm.value_ptr(MVP))
        glUniformMatrix4fv(model_location, 1, GL_FALSE, glm.value_ptr(self.trans))
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def __del__(self):
        super().__del__()
        self.bitmap_handler.delete_texture(self.texture)
