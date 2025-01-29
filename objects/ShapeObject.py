import numpy as np
from objects.TransformableObject import *
from objects.DrawableObject import *
import glm
from objects.GameObject import *


class ShapeObject(TransformableObject, DrawableObject):
    """
    A base class combining transformation and drawing capabilities.

    Inherits from TransformableObject and DrawableObject to create renderable 3D objects.

    Attributes:
        vertices (numpy.ndarray): Vertex data for the shape
        vertex_shader_source (str): Vertex shader source code
        fragment_shader_source (str): Fragment shader source code
        draw_mode (int): OpenGL drawing mode (e.g. GL_TRIANGLES)
    """

    def __init__(
        self,
        vertices,
        vertex_shader_source,
        fragment_shader_source,
        draw_mode=GL_TRIANGLES,
    ):
        """
        Initialize a shape object.

        Args:
            vertices (numpy.ndarray): Vertex data for the shape
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader
            draw_mode (int): OpenGL drawing mode, defaults to GL_TRIANGLES
        """
        TransformableObject.__init__(self)
        DrawableObject.__init__(
            self,
            vertices,
            vertex_shader_source,
            fragment_shader_source,
            draw_mode=GL_TRIANGLES,
        )
