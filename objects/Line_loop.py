import numpy as np
from .GameObject import *
import glm

"""
A class for rendering connected line loops in OpenGL.

This class extends OpenGLObject to render a series of connected lines that form a closed loop.

Attributes:
    vertices (numpy.ndarray): Vertex data for the line points
    vertex_shader_source (str): Source code for vertex shader
    fragment_shader_source (str): Source code for fragment shader
"""

class LineLoop(OpenGLObject):
    def __init__(self, points, vertex_shader_source, fragment_shader_source):
        """
        Initialize a LineLoop object.

        Args:
            points (list): List of vertex positions forming the line loop
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader
        """
        vertices = np.array(points, dtype=np.float32).flatten()
        super().__init__(vertices, vertex_shader_source, fragment_shader_source, draw_mode=GL_LINE_LOOP)
