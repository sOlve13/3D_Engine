import numpy as np
from objects.GameObject import *
import glm

import ctypes

"""
A class for rendering a light source cube in OpenGL.

This class extends OpenGLObject to render a small cube representing a light source.

Attributes:
    trans (glm.mat4): Transformation matrix
    vertices (numpy.ndarray): Vertex data for the cube
"""

class LightCube(OpenGLObject):
    def __init__(self, vertex_shader_source, fragment_shader_source):
        """
        Initialize a LightCube object.

        Args:
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader
        """
        self.trans = glm.mat4(1.0)
        
        scale = 0.2
        self.vertices = np.array([
            -0.5 * scale, -0.5 * scale, -0.5 * scale,
             0.5 * scale, -0.5 * scale, -0.5 * scale,
             0.5 * scale,  0.5 * scale, -0.5 * scale,
             0.5 * scale,  0.5 * scale, -0.5 * scale,
            -0.5 * scale,  0.5 * scale, -0.5 * scale,
            -0.5 * scale, -0.5 * scale, -0.5 * scale,

            -0.5 * scale, -0.5 * scale,  0.5 * scale,
             0.5 * scale, -0.5 * scale,  0.5 * scale,
             0.5 * scale,  0.5 * scale,  0.5 * scale,
             0.5 * scale,  0.5 * scale,  0.5 * scale,
            -0.5 * scale,  0.5 * scale,  0.5 * scale,
            -0.5 * scale, -0.5 * scale,  0.5 * scale,

            -0.5 * scale,  0.5 * scale,  0.5 * scale,
            -0.5 * scale,  0.5 * scale, -0.5 * scale,
            -0.5 * scale, -0.5 * scale, -0.5 * scale,
            -0.5 * scale, -0.5 * scale, -0.5 * scale,
            -0.5 * scale, -0.5 * scale,  0.5 * scale,
            -0.5 * scale,  0.5 * scale,  0.5 * scale,

             0.5 * scale,  0.5 * scale,  0.5 * scale,
             0.5 * scale,  0.5 * scale, -0.5 * scale,
             0.5 * scale, -0.5 * scale, -0.5 * scale,
             0.5 * scale, -0.5 * scale, -0.5 * scale,
             0.5 * scale, -0.5 * scale,  0.5 * scale,
             0.5 * scale,  0.5 * scale,  0.5 * scale,

            -0.5 * scale, -0.5 * scale, -0.5 * scale,
             0.5 * scale, -0.5 * scale, -0.5 * scale,
             0.5 * scale, -0.5 * scale,  0.5 * scale,
             0.5 * scale, -0.5 * scale,  0.5 * scale,
            -0.5 * scale, -0.5 * scale,  0.5 * scale,
            -0.5 * scale, -0.5 * scale, -0.5 * scale,

            -0.5 * scale,  0.5 * scale, -0.5 * scale,
             0.5 * scale,  0.5 * scale, -0.5 * scale,
             0.5 * scale,  0.5 * scale,  0.5 * scale,
             0.5 * scale,  0.5 * scale,  0.5 * scale,
            -0.5 * scale,  0.5 * scale,  0.5 * scale,
            -0.5 * scale,  0.5 * scale, -0.5 * scale
        ], dtype=np.float32)

        super().__init__(self.vertices, vertex_shader_source, fragment_shader_source)

    def _setup_buffers(self):
        """
        Set up vertex buffer objects and attributes.
        
        Configures vertex position attribute (layout 0).
        """
        glBindVertexArray(self.VAO)
        
        # Настраиваем буфер вершин
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        # Позиции вершин
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self, projection_matrix, view, light_pos):
        """
        Draw the light cube.

        Args:
            projection_matrix (glm.mat4): Camera projection matrix
            view (glm.mat4): Camera view matrix
            light_pos (tuple): XYZ position where the light cube should be drawn
        """
        glUseProgram(self.shader_program)
        
        self.trans = glm.mat4(1.0)
        self.trans = glm.translate(self.trans, glm.vec3(light_pos[0], light_pos[1], light_pos[2]))
        
        MVP = projection_matrix * view * self.trans
        mvp_location = glGetUniformLocation(self.shader_program, "MVP")
        
        glUniformMatrix4fv(mvp_location, 1, GL_FALSE, glm.value_ptr(MVP))
        
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)

    def __del__(self):
        """Clean up OpenGL resources."""
        glDeleteBuffers(1, [self.VBO])
        glDeleteVertexArrays(1, [self.VAO])

    def scale(self, scale):
        """
        Scale the light cube uniformly.

        Args:
            scale (float): Scale factor to apply in all dimensions
        """
        scale_matrix = glm.scale(glm.mat4(1.0), glm.vec3(scale, scale, scale))
        self.trans *= scale_matrix

    def rotate(self, angle_x, angle_y, angle_z):
        """
        Rotate the light cube around all axes.

        Args:
            angle_x (float): Rotation angle around X axis in degrees
            angle_y (float): Rotation angle around Y axis in degrees
            angle_z (float): Rotation angle around Z axis in degrees
        """
        self.trans = glm.rotate(
            self.trans, glm.radians(angle_x), glm.vec3(1.0, 0.0, 0.0)
        )
        self.trans = glm.rotate(
            self.trans, glm.radians(angle_y), glm.vec3(0.0, 1.0, 0.0)
        )
        self.trans = glm.rotate(
            self.trans, glm.radians(angle_z), glm.vec3(0.0, 0.0, 1.0)
        )

    def translate(self, x, y):
        """
        Translate the light cube in XY plane.

        Args:
            x (float): Translation along X axis
            y (float): Translation along Y axis
        """
        self.trans = glm.translate(self.trans, glm.vec3(x, y, 0))
