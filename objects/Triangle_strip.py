import numpy as np
from .GameObject import *
import glm

class TriangleStrip(OpenGLObject):
    def __init__(self, points, vertex_shader_source, fragment_shader_source):
        vertices = np.array(points, dtype=np.float32).flatten()
        super().__init__(vertices, vertex_shader_source, fragment_shader_source, draw_mode=GL_TRIANGLE_STRIP)
