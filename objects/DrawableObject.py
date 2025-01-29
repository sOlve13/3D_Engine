import numpy as np
from objects.GameObject import *
import glm


"""
A base class for objects that can be rendered in OpenGL.

Provides basic functionality for shader compilation, buffer setup, and drawing.

Attributes:
    vertices (numpy.ndarray): Vertex data for the object
    vertex_shader_source (str): Source code for vertex shader
    fragment_shader_source (str): Source code for fragment shader
    draw_mode (int): OpenGL drawing mode (e.g., GL_TRIANGLES)
    VAO (int): Vertex Array Object ID
    VBO (int): Vertex Buffer Object ID
    shader_program (int): Compiled shader program ID
"""

class DrawableObject:
    def __init__(
        self,
        vertices,
        vertex_shader_source,
        fragment_shader_source,
        draw_mode=GL_TRIANGLES,
    ):
        """
        Initialize a drawable object.

        Args:
            vertices (numpy.ndarray): Vertex data
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader
            draw_mode (int): OpenGL drawing mode, defaults to GL_TRIANGLES
        """
        self.vertices = vertices
        self.vertex_shader_source = vertex_shader_source
        self.fragment_shader_source = fragment_shader_source
        self.draw_mode = draw_mode

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.shader_program = self._create_shader_program()

        self._setup_buffers()

    def _setup_buffers(self):
        """
        Set up vertex buffer objects and attributes.

        Configures vertex attributes for:
        - Position (layout 0)
        - Color/Normal (layout 1)
        """
        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(
            GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW
        )
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * np.dtype(np.float32).itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * np.dtype(np.float32).itemsize, ctypes.c_void_p(3 * np.dtype(np.float32).itemsize))
        glEnableVertexAttribArray(1)

        glBindVertexArray(0)

    def _compile_shader(self, shader_type, source):
        """
        Compile a shader from source.

        Args:
            shader_type (int): GL_VERTEX_SHADER or GL_FRAGMENT_SHADER
            source (str): Shader source code

        Returns:
            int: Compiled shader ID

        Raises:
            Exception: If shader compilation fails
        """
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error_log = glGetShaderInfoLog(shader)
            raise Exception(f"Shader compilation failed : {error_log.decode()}")

        return shader

    def _create_shader_program(self):
        """
        Create and link shader program.

        Returns:
            int: Linked shader program ID

        Raises:
            Exception: If program linking fails
        """
        vertex_shader = self._compile_shader(
            GL_VERTEX_SHADER, self.vertex_shader_source
        )
        fragment_shader = self._compile_shader(
            GL_FRAGMENT_SHADER, self.fragment_shader_source
        )

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

    def draw(self, projection_matrix, view):
        """
        Draw the object.

        Args:
            projection_matrix (glm.mat4): Camera projection matrix
            view (glm.mat4): Camera view matrix
        """
        glUseProgram(self.shader_program)
        light_pos_location = glGetUniformLocation(self.shader_program, "lightPos")
        light_pos = [1.0, 1.0, 1.0]
        glUniform3f(light_pos_location, *light_pos)
        MVP = projection_matrix * view * self.trans
        mvp_location = glGetUniformLocation(self.shader_program, "MVP")
        glUniformMatrix4fv(mvp_location, 1, GL_FALSE, glm.value_ptr(MVP))
        glBindVertexArray(self.VAO)
        glDrawArrays(self.draw_mode, 0, len(self.vertices) // 3)

        glBindVertexArray(0)

    def __del__(self):
        """Clean up OpenGL resources on deletion."""
        glDeleteBuffers(1, [self.VBO])
        glDeleteVertexArrays(1, [self.VAO])
        glDeleteProgram(self.shader_program)
