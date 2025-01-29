import numpy as np
from OpenGL.GL import *
from objects.ShapeObject import *
from objects.UpdatableObject import *

import glm


"""
A base class combining shape, transformation and update capabilities.

This class inherits from ShapeObject and UpdatableObject to create interactive 3D objects.

Attributes:
    vertices (numpy.ndarray): Vertex data for the object
    vertex_shader_source (str): Source code for vertex shader
    fragment_shader_source (str): Source code for fragment shader
    draw_mode (int): OpenGL drawing mode (e.g. GL_TRIANGLES)
    update_count (int): Number of updates performed
"""

class OpenGLObject(ShapeObject, UpdataleObject):
    def __init__(
        self,
        vertices,
        vertex_shader_source,
        fragment_shader_source,
        draw_mode=GL_TRIANGLES,
    ):
        """
        Initialize an OpenGL object.

        Args:
            vertices (numpy.ndarray): Vertex data for the object
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader
            draw_mode (int): OpenGL drawing mode, defaults to GL_TRIANGLES
        """
        ShapeObject.__init__(
            self,
            vertices,
            vertex_shader_source,
            fragment_shader_source,
            draw_mode=GL_TRIANGLES,
        )
        UpdataleObject.__init__(self)
