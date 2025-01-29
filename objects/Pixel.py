import numpy as np
from .GameObject import *
import glm

"""
A class for rendering individual pixels in OpenGL.

This class extends OpenGLObject to render single points/pixels.

Attributes:
    vertices (numpy.ndarray): Single vertex position data
    vertex_shader_source (str): Vertex shader source code
    fragment_shader_source (str): Fragment shader source code
"""

class Pixel(OpenGLObject):
    def __init__(self, position, vertex_shader_source, fragment_shader_source):
        """
        Initialize a Pixel object.

        Args:
            position (tuple): XYZ coordinates of the pixel
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader
        """
        vertices = np.array([
            *position  
        ], dtype=np.float32)
        super().__init__(vertices, vertex_shader_source, fragment_shader_source, draw_mode=GL_POINTS)
