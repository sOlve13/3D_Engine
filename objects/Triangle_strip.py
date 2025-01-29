import numpy as np
from objects.GameObject import *
import glm

"""
A class for rendering triangle strips in OpenGL.

This class extends OpenGLObject to render connected triangles in strip format.

Attributes:
    trans (glm.mat4): Transformation matrix
    vertices (numpy.ndarray): Vertex data for the triangle strip
    
Methods:
    draw(projection_matrix, view): Renders the triangle strip with given matrices
"""

class Triangle_strip(OpenGLObject):
    def __init__(self, points, vertex_shader_source, fragment_shader_source):
        self.trans = glm.mat4(1.0)
        vertices = np.array(points, dtype=np.float32)
        super().__init__(vertices, vertex_shader_source, fragment_shader_source)
        
    def draw(self, projection_matrix, view):
        glUseProgram(self.shader_program)
        MVP = projection_matrix * view * self.trans
        mvp_location = glGetUniformLocation(self.shader_program, "MVP")
        glUniformMatrix4fv(mvp_location, 1, GL_FALSE, glm.value_ptr(MVP))
        
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, len(self.vertices) // 3)
        glBindVertexArray(0)
