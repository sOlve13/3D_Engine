import numpy as np
from objects.GameObject import *
import glm
from objects.BitmapHandler import BitmapHandler
import ctypes

"""
A class for rendering a textured cube in OpenGL.

This class extends OpenGLObject to render a cube with texture mapping and lighting.

Attributes:
    trans (glm.mat4): Transformation matrix
    vertices (numpy.ndarray): Vertex data including positions, normals and texture coordinates
    indices (numpy.ndarray): Index data for triangle faces
    texture (int): OpenGL texture ID
    bitmap_handler (BitmapHandler): Handler for texture loading and management
"""

class TexturedCube(OpenGLObject):
    def __init__(self, vertex_shader_source, fragment_shader_source, texture_path):
        """
        Initialize a TexturedCube object.

        Args:
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader
            texture_path (str): Path to texture image file
        """
        self.trans = glm.mat4(1.0)
        self.vertices = np.array([
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  1.0, 0.0,
             0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0, 1.0,
            -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0, 0.0,
             0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  0.0, 1.0,
            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0, 0.0,
            -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,  1.0, 1.0,
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0, 1.0,
            -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,  0.0, 0.0,
             0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0, 0.0,
             0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  1.0, 1.0,
             0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0, 1.0,
             0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0, 1.0,
             0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  1.0, 1.0,
             0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0, 1.0,
             0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  1.0, 1.0,
             0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  0.0, 0.0
        ], dtype=np.float32)

        self.indices = np.array([
            0,  1,  2,  2,  3,  0,
            4,  5,  6,  6,  7,  4,
            8,  9,  10, 10, 11, 8,
            12, 13, 14, 14, 15, 12,
            16, 17, 18, 18, 19, 16,
            20, 21, 22, 22, 23, 20
        ], dtype=np.uint32)

        super().__init__(self.vertices, vertex_shader_source, fragment_shader_source)

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        self.bitmap_handler = BitmapHandler()
        self.texture = self.bitmap_handler.load_texture(texture_path)

    def _setup_buffers(self):
        """
        Set up vertex buffer objects and attributes.
        
        Configures vertex attributes for:
        - Position (layout 0)
        - Normal (layout 1)
        - Texture coordinates (layout 2)
        """
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
        """
        Draw the textured cube with lighting.

        Args:
            projection_matrix (glm.mat4): Camera projection matrix
            view (glm.mat4): Camera view matrix
            camera_position (tuple): XYZ position of camera
            light_pos (tuple): XYZ position of light source
        """
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
        """
        Clean up OpenGL resources.
        Deletes texture and calls parent destructor.
        """
        super().__del__()
        self.bitmap_handler.delete_texture(self.texture)
