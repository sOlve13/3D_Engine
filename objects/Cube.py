import numpy as np
from objects.GameObject import *
import glm

def get_uniform_value(shader_program, uniform_name):
    location = glGetUniformLocation(shader_program, uniform_name)
    if location == -1:
        print(f"Uniform '{uniform_name}' не найден в программе.")
        return None
    value = np.zeros((16,), dtype=np.float32)
    try:
        glGetUniformfv(shader_program, location, value)
        print(f"Uniform '{uniform_name}' имеет значение: {value}")
        return value
    except Exception as e:
        print(f"Ошибка при чтении значения униформы '{uniform_name}': {e}")
        return None

import ctypes

"""
A class for rendering a cube with lighting in OpenGL.

This class extends OpenGLObject to render a cube with basic lighting calculations.

Attributes:
    trans (glm.mat4): Transformation matrix
    vertices (numpy.ndarray): Vertex data including positions and normals
    indices (numpy.ndarray): Index data for triangle faces
    colors (numpy.ndarray): Color data for cube faces
    normals (numpy.ndarray): Normal vectors for lighting calculations
"""

class Cube(OpenGLObject):
    def __init__(self, vertex_shader_source, fragment_shader_source):
        """
        Initialize a Cube object.

        Args:
            vertex_shader_source (str): Source code for vertex shader
            fragment_shader_source (str): Source code for fragment shader
        """
        self.trans = glm.mat4(1.0)
        self.vertices = np.array([
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
             0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
             0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
            -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
             0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
             0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
            -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
            -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,
            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,
            -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
             0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
             0.5,  0.5, -0.5,  1.0,  0.0,  0.0,
             0.5,  0.5,  0.5,  1.0,  0.0,  0.0,
             0.5, -0.5,  0.5,  1.0,  0.0,  0.0,
            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
             0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
             0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
            -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
             0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
             0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
            -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
        ], dtype=np.float32)

        self.indices = np.array([
            0,  1,  2,  2,  3,  0,
            4,  5,  6,  6,  7,  4,
            8,  9,  10, 10, 11, 8,
            12, 13, 14, 14, 15, 12,
            16, 17, 18, 18, 19, 16,
            20, 21, 22, 22, 23, 20
        ], dtype=np.uint32)

        self.colors = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.0, 1.0, 0.0],
                [1.0, 0.0, 1.0],
                [0.0, 1.0, 1.0],
                [1.0, 1.0, 1.0],
                [0.0, 0.0, 0.0],
            ],
            dtype=np.float32,
        )

        self.normals = np.array(
            [
                [0.0, 0.0, -1.0],
                [0.0, 0.0, 1.0],
                [-1.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, -1.0, 0.0],
            ],
            dtype=np.float32,
        )

        super().__init__(self.vertices, vertex_shader_source, fragment_shader_source)

        self.shader_program = super()._create_shader_program()

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def _setup_buffers(self):
        """
        Set up vertex buffer objects and attributes.

        Configures vertex attributes for:
        - Position (layout 0)
        - Normal (layout 1)
        """
        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self, projection_matrix, view, camera_position, light_pos):
        """
        Draw the cube with lighting.

        Args:
            projection_matrix (glm.mat4): Camera projection matrix
            view (glm.mat4): Camera view matrix
            camera_position (tuple): XYZ position of camera
            light_pos (tuple): XYZ position of light source
        """
        glUseProgram(self.shader_program)

        light_pos = light_pos
        light_color = [1.0, 1.0, 1.0]
        object_color = [0.8, 0.1, 0.1]
        view_pos = camera_position

        glUniform3f(glGetUniformLocation(self.shader_program, "lightPos"), *light_pos)
        glUniform3f(glGetUniformLocation(self.shader_program, "lightColor"), *light_color)
        glUniform3f(glGetUniformLocation(self.shader_program, "objectColor"), *object_color)
        glUniform3f(glGetUniformLocation(self.shader_program, "viewPos"), *view_pos)

        MVP = projection_matrix * view * self.trans
        mvp_location = glGetUniformLocation(self.shader_program, "MVP")
        model_location = glGetUniformLocation(self.shader_program, "model")

        glUniformMatrix4fv(mvp_location, 1, GL_FALSE, glm.value_ptr(MVP))
        glUniformMatrix4fv(model_location, 1, GL_FALSE, glm.value_ptr(self.trans))

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

        glBindVertexArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def __del__(self):
        """Clean up OpenGL resources."""
        try:
            if hasattr(self, 'VBO'):
                glDeleteBuffers(1, [self.VBO])
            if hasattr(self, 'VAO'):
                glDeleteVertexArrays(1, [self.VAO])
        except:
            pass

    def scale(self, scale):
        """
        Scale the cube uniformly.

        Args:
            scale (float): Scale factor to apply in all dimensions
        """
        scale_matrix = glm.scale(glm.mat4(1.0), glm.vec3(scale, scale, scale))
        self.trans *= scale_matrix

    def rotate(self, angle_x, angle_y, angle_z):
        """
        Rotate the cube around all axes.

        Args:
            angle_x (float): Rotation angle around X axis in degrees
            angle_y (float): Rotation angle around Y axis in degrees
            angle_z (float): Rotation angle around Z axis in degrees
        """
        self.trans = glm.rotate(
            self.trans, glm.radians(angle_x), glm.vec3(1.0, 0.0, 0.0)
        )
        self.trans = glm.rotate(
            self.trans, glm.radians(angle_y), glm.vec3(0.0, 1.0, 0.0)
        )
        self.trans = glm.rotate(
            self.trans, glm.radians(angle_z), glm.vec3(0.0, 0.0, 1.0)
        )

    def translate(self, x, y):
        """
        Translate the cube in XY plane.

        Args:
            x (float): Translation along X axis
            y (float): Translation along Y axis
        """
        self.trans = glm.translate(self.trans, glm.vec3(x, y, 0))
