import numpy as np
from OpenGL.GL import *
import glm

class OpenGLObject:
    def __init__(self, vertices, vertex_shader_source, fragment_shader_source, draw_mode=GL_TRIANGLES):
        self.vertices = vertices
        self.vertex_shader_source = vertex_shader_source
        self.fragment_shader_source = fragment_shader_source
        self.draw_mode = draw_mode

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.shader_program = self._create_shader_program()

        self._setup_buffers()

    def _setup_buffers(self):
        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * self.vertices.itemsize, None)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

    def _compile_shader(self, shader_type, source):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error_log = glGetShaderInfoLog(shader)
            raise Exception(f"Shader compilation failed : {error_log.decode()}")

        return shader

    def _create_shader_program(self):
        vertex_shader = self._compile_shader(GL_VERTEX_SHADER, self.vertex_shader_source)
        fragment_shader = self._compile_shader(GL_FRAGMENT_SHADER, self.fragment_shader_source)

        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)

        if not glGetProgramiv(program, GL_LINK_STATUS):
            error_log = glGetProgramInfoLog(program)
            raise Exception(f"Shader program linking failed : {error_log.decode()}")

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        return program

    def draw(self):
        glUseProgram(self.shader_program)

        glBindVertexArray(self.VAO)
        glDrawArrays(self.draw_mode, 0, len(self.vertices) // 3)

        glBindVertexArray(0)

    def __del__(self):
        glDeleteBuffers(1, [self.VBO])
        glDeleteVertexArrays(1, [self.VAO])
        glDeleteProgram(self.shader_program)
