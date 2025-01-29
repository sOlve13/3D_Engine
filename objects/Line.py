import numpy as np
from .GameObject import *
import glm

"""
A class for rendering lines in OpenGL.

This class extends OpenGLObject to render line segments between two points.

Attributes:
    vertices (numpy.ndarray): Start and end point vertex data
    vertex_shader_source (str): Source code for vertex shader
    fragment_shader_source (str): Source code for fragment shader
"""

class Line(OpenGLObject):
    def __init__(self, start, end, vertex_shader_source, fragment_shader_source):
        """
        Initialize a Line object.

        Args:
            start (tuple): XYZ coordinates of line start point
            end (tuple): XYZ coordinates of line end point
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader
        """
        vertices = np.array([
            *start, 
            *end    
        ], dtype=np.float32)
        super().__init__(vertices, vertex_shader_source, fragment_shader_source, draw_mode=GL_LINES)

# check pros and cons of list and numpy array