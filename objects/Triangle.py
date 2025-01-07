import numpy as np
from .GameObject import *
import glm

class Triangle(OpenGLObject):
    def __init__(self, vertices, vertex_shader_source, fragment_shader_source):
        super().__init__(vertices, vertex_shader_source, fragment_shader_source, draw_mode=GL_TRIANGLES)
