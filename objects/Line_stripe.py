import numpy as np
from .GameObject import *
import glm

"""
A class for rendering connected line strips in OpenGL.

This class extends OpenGLObject to render a series of connected line segments.
Each vertex is connected to the next vertex in sequence, forming a continuous strip.

Attributes:
    vertices (numpy.ndarray): Vertex data for the line strip points
    vertex_shader_source (str): Source code for vertex shader
    fragment_shader_source (str): Source code for fragment shader
"""

class LineStripe(OpenGLObject):
    def __init__(self, points, vertex_shader_source, fragment_shader_source):
        """
        Initialize a LineStripe object.

        Args:
            points (list): List of vertex positions forming the line strip
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader

        Note:
            Points are connected in sequence: point[0] to point[1], point[1] to point[2], etc.
        """
        vertices = np.array(points, dtype=np.float32).flatten()
        super().__init__(vertices, vertex_shader_source, fragment_shader_source, draw_mode=GL_LINE_STRIP)
