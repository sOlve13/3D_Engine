import numpy as np
from .GameObject import *
import glm

class Line(OpenGLObject):
    def __init__(self, start, end, vertex_shader_source, fragment_shader_source):
        vertices = np.array([
            *start, 
            *end    
        ], dtype=np.float32)
        super().__init__(vertices, vertex_shader_source, fragment_shader_source, draw_mode=GL_LINES)

# check pros and cons of list and numpy array