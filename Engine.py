import glfw
from OpenGL.GL import *
import random
from Window import Window
import glm
import time

class Engine:
    def __init__(self, width, height, title, fullscreen=False, fps=60):
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

    def initialize(self):
        if not glfw.init():
            raise Exception("GLFW could not be initialized!")

        self.window = Window(self.width, self.height, self.title, None, None)
        self.window.setup()

        glfw.set_key_callback(self.window.getWindow(), self.key_callback)
        glfw.set_mouse_button_callback(self.window.getWindow(), self.mouse_button_callback)
        glfw.set_cursor_pos_callback(self.window.getWindow(), self.cursor_position_callback)
        glfw.set_char_callback(self.window.getWindow(), self.text_input_callback)

        # Enable depth testing
        glEnable(GL_DEPTH_TEST)

    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            self.background_color = [random.random(), random.random(), random.random(), 1.0]
        elif key == glfw.KEY_E and action == glfw.PRESS:
            self.background_color = [0.2, 0.2, 0.2, 1.0]
        elif key == glfw.KEY_BACKSPACE and (action == glfw.PRESS or action == glfw.REPEAT):
            self.input_text = self.input_text[:-1]

    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            self.background_color = [random.random(), random.random(), random.random(), 1.0]

    def cursor_position_callback(self, window, xpos, ypos):
        self.background_color = [xpos / self.width, ypos / self.height, 0.5, 1.0]

    def text_input_callback(self, window, character):
        self.input_text += chr(character)

    def set_projection(self, fov, aspect, zNear, zFar, type):
        if type == 1:
            self.projection_matrix = glm.perspective(glm.radians(fov), aspect, zNear, zFar)
        else:
            self.projection_matrix = glm.ortho(-aspect, aspect, -1.0, 1.0, zNear, zFar)

    def main_loop(self):
        while not glfw.window_should_close(self.window.getWindow()):
            currentTime = glfw.get_time()
            self.frameCount += 1
            if (currentTime - self.previousTime) >= 1.0:
                glfw.set_window_title(self.window.getWindow(), f"FPS: {self.frameCount}")
                self.frameCount = 0
                self.previousTime = currentTime

            if self.input_text == "black":
                self.background_color = [0, 0, 0, 1]

            glClearColor(*self.background_color)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


            glfw.swap_buffers(self.window.getWindow())
            glfw.poll_events()

            elapsed_time = glfw.get_time() - currentTime
            if elapsed_time < self.frame_duration:
                time.sleep(self.frame_duration - elapsed_time)

    def terminate(self):
        glfw.terminate()
