import numpy as np
from .GameObject import *
import glm

"""
A class representing a triangle object in OpenGL.

This class extends OpenGLObject to render a basic triangle shape.

Attributes:
    vertices (numpy.ndarray): The vertex data for the triangle
    vertex_shader_source (str): Source code for the vertex shader
    fragment_shader_source (str): Source code for the fragment shader
"""

class Triangle(OpenGLObject):
    def __init__(self, vertices, vertex_shader_source, fragment_shader_source):
        """
        Initialize a Triangle object.

        Args:
            vertices (numpy.ndarray): Array of vertex positions
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader
        """
        super().__init__(vertices, vertex_shader_source, fragment_shader_source, draw_mode=GL_TRIANGLES)
