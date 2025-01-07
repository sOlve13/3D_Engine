import numpy as np
from .GameObject import *
import glm

class Pixel(OpenGLObject):
    def __init__(self, position, vertex_shader_source, fragment_shader_source):
        vertices = np.array([
            *position  
        ], dtype=np.float32)
        super().__init__(vertices, vertex_shader_source, fragment_shader_source, draw_mode=GL_POINTS)
