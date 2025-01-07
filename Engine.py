import glfw
from OpenGL.GL import *
import random
from Window import Window
import glm
import time
import numpy as np
from objects.Line import *
from objects.Triangle import *
from objects.Pixel import *
from objects.Line_loop import *
from objects.Line_stripe import *
from objects.Triangle_strip import *
from objects.Triangle_fans import *
from objects.Cube import *


class Engine:
    def __init__(self, width, height, title, fullscreen=False, fps=60):
        if not glfw.init():
            raise Exception("GLFW could not be initialized!")
        self.width = width
        self.height = height
        self.title = title
        self.fullscreen = fullscreen
        self.window = None
        self.background_color = [0.1, 0.2, 0.3, 1.0]
        self.input_text = ""
        self.frameCount = 0
        self.previousTime = glfw.get_time()
        self.projection_matrix = glm.mat4(1.0)
        self.fps = fps
        self.frame_duration = 1.0 / fps
        self.window_should_close = False
    def initialize(self):

        self.window = Window(self.width, self.height, self.title, self.fullscreen, None)
        self.window.setup()

        glfw.set_key_callback(self.window.getWindow(), self.key_callback)
        glfw.set_mouse_button_callback(self.window.getWindow(), self.mouse_button_callback)
        glfw.set_cursor_pos_callback(self.window.getWindow(), self.cursor_position_callback)
        glfw.set_char_callback(self.window.getWindow(), self.text_input_callback)
        glfw.set_scroll_callback(self.window.getWindow(), self.scroll_callback)

    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            self.background_color = [random.random(), random.random(), random.random(), 1.0]
        elif key == glfw.KEY_E and action == glfw.PRESS:
            self.background_color = [0.2, 0.2, 0.2, 1.0]
        elif key == glfw.KEY_BACKSPACE and (action == glfw.PRESS or action == glfw.REPEAT):
            self.input_text = self.input_text[:-1]
        elif key == glfw.KEY_1 and action == glfw.PRESS:
            self.window_should_close = True  

    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            self.background_color = [random.random(), random.random(), random.random(), 1.0]

    def cursor_position_callback(self, window, xpos, ypos):
        self.background_color = [xpos / self.width, ypos / self.height, 0.5, 1.0]

    def scroll_callback(self, window, xoffset, yoffset):
        self.background_color = [yoffset / 0.5, yoffset / 1.0, 1, 1.0]

    def text_input_callback(self, window, character):
        self.input_text += chr(character)

    def set_projection(self, fov, aspect, zNear, zFar, type):
        if type == 1:
            self.projection_matrix = glm.perspective(glm.radians(fov), aspect, zNear, zFar)
        else:
            self.projection_matrix = glm.ortho(-aspect, aspect, -1.0, 1.0, zNear, zFar)

    def draw(self):
        vertices = np.array([
            -0.5, -0.5, 0,
            0.5, -0.5, 0,
            0.0, 0.5, 0
        ], dtype=np.float32)

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, None)
        glEnableVertexAttribArray(0)

        vertexShaderSource = """
        #version 330 core
        layout (location = 0) in vec3 aPos;
        void main()
        {
           gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
        }
        """

        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, vertexShaderSource)
        glCompileShader(vertexShader)

        if not glGetShaderiv(vertexShader, GL_COMPILE_STATUS):
            raise Exception(glGetShaderInfoLog(vertexShader))

        fragmentShaderSource = """
        #version 330 core
        out vec4 FragColor;
        void main()
        {
            FragColor = vec4(1.0, 0.5, 0.2, 1.0);
        }
        """

        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, fragmentShaderSource)
        glCompileShader(fragmentShader)

        if not glGetShaderiv(fragmentShader, GL_COMPILE_STATUS):
            raise Exception(glGetShaderInfoLog(fragmentShader))

        shaderProgram = glCreateProgram()
        glAttachShader(shaderProgram, vertexShader)
        glAttachShader(shaderProgram, fragmentShader)
        glLinkProgram(shaderProgram)

        if not glGetProgramiv(shaderProgram, GL_LINK_STATUS):
            raise Exception(glGetProgramInfoLog(shaderProgram))

        glUseProgram(shaderProgram)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)

    def main_loop(self):
        while not glfw.window_should_close(self.window.getWindow()) and not self.window_should_close:
            width, height = glfw.get_window_size(self.window.getWindow())
            glViewport(0, 0, width, height)
            currentTime = glfw.get_time()
            self.frameCount += 1
            if (currentTime - self.previousTime) >= 1.0:
                glfw.set_window_title(self.window.getWindow(), f"FPS: {self.frameCount}")
                self.frameCount = 0
                self.previousTime = currentTime

            if self.input_text == "black":
                self.background_color = [0, 0, 0, 1]

            glClearColor(*self.background_color)
            glClear(GL_COLOR_BUFFER_BIT)

            vertex_shader_source = """
            #version 330 core
            layout (location = 0) in vec3 aPos;
            out vec2 FragCoordinates;
            void main()
            {
                gl_Position = vec4(aPos, 1.0);
                FragCoordinates = aPos.xy;
            }
            """

            fragment_shader_source = """
            #version 330 core
            in vec2 FragCoordinates;
            out vec4 FragColor;
            void main()
            {
                float gradx = (FragCoordinates.x + 1.0) / 2.0;
                float grady = (FragCoordinates.y + 1.0) / 2.0;
                vec3 color = vec3(gradx, grady, 1.0 - grady);
                FragColor = vec4(color, 1.0);
            }
            """

            triangle_vertices = np.array([
                -0.5, -0.5, 0.0,
                    0.5, -0.5, 0.0,
                    0.0,  0.5, 0.0
            ], dtype=np.float32)

            triangle = Triangle(triangle_vertices, vertex_shader_source, fragment_shader_source)

            line = Line([-0.5, 0.0, 0.0], [0.5, 0.0, 0.0], vertex_shader_source, fragment_shader_source)

            pixel = Pixel([0.0, 0.0, 0.0], vertex_shader_source, fragment_shader_source)

            line_points = [
                [-0.5, 0.0, 0.0],
                [-0.25, 0.5, 0.0],
                [0.25, -0.5, 0.0],
                [0.5, 0.0, 0.0]
            ]
            line_stripe = LineStripe(line_points, vertex_shader_source, fragment_shader_source)


            line_loop_points = [
                [-0.5, -0.5, 0.0],
                [0.5, -0.5, 0.0],
                [0.0,  0.5, 0.0]
            ]
            line_loop = LineLoop(line_loop_points, vertex_shader_source, fragment_shader_source)

            triangle_strip_points = [
                [-0.5, -0.5, 0.0],
                [0.5, -0.5, 0.0],
                [0.0,  0.5, 0.0],
                [0.5,  0.5, 0.0],
                [0.7, 0.0, 0.0],
            ]
            triangle_strip = TriangleStrip(triangle_strip_points, vertex_shader_source, fragment_shader_source)

            triangle_fan_points = [
                [0.0,  0.0, 0.0],
                [-0.5, -0.5, 0.0],
                [0.5, -0.5, 0.0],
                [0.0,  0.5, 0.0],
                [-0.5, 0.3, 0.0],
            ]
            triangle_fan = TriangleFan(triangle_fan_points, vertex_shader_source, fragment_shader_source)
            cube = Cube(vertex_shader_source, fragment_shader_source)
            #cube.draw()
            #triangle_fan.draw()
            triangle_strip.draw()

            glfw.swap_buffers(self.window.getWindow())
            glfw.poll_events()

            elapsed_time = glfw.get_time() - currentTime
            if elapsed_time < self.frame_duration:
                time.sleep(self.frame_duration - elapsed_time)

    def terminate(self):
        glfw.terminate()
