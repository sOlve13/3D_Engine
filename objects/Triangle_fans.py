import numpy as np
from objects.GameObject import *
import glm


class Triangle_fans(OpenGLObject):
    """
    A class for rendering triangle fans in OpenGL.

    This class extends OpenGLObject to render triangle fans from a set of points.

    Attributes:
        trans (glm.mat4): Transformation matrix
        vertices (numpy.ndarray): Vertex data for the triangle fan
        
    Methods:
        draw(projection_matrix, view): Renders the triangle fan with given matrices
    """
    def __init__(self, points, vertex_shader_source, fragment_shader_source):
        """
        Initialize a Triangle Fan object.

        Args:
            points (list): List of vertex positions for the triangle fan
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader
        """
        self.trans = glm.mat4(1.0)
        vertices = np.array(points, dtype=np.float32)
        super().__init__(vertices, vertex_shader_source, fragment_shader_source)
        
    def draw(self, projection_matrix, view):
        """
        Draw the triangle fan.

        Args:
            projection_matrix (glm.mat4): Projection matrix for the scene
            view (glm.mat4): View matrix for the camera
        """
        glUseProgram(self.shader_program)
        MVP = projection_matrix * view * self.trans
        mvp_location = glGetUniformLocation(self.shader_program, "MVP")
        glUniformMatrix4fv(mvp_location, 1, GL_FALSE, glm.value_ptr(MVP))
        
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLE_FAN, 0, len(self.vertices) // 3)
        glBindVertexArray(0)
