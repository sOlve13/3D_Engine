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
from objects.CameraObject import *
from objects.lightCube import *
from Shaders import *
from objects.TexturedCube import *
from objects.TexturedSphere import *


class Engine:
    """
    Main game engine class that handles window creation, rendering, and input processing.
    
    This class manages the game loop, shader loading, object rendering, and user input handling.
    It serves as the central coordinator for the OpenGL-based application.

    Attributes:
        width (int): Window width in pixels
        height (int): Window height in pixels
        title (str): Window title
        fullscreen (bool): Whether the window should be fullscreen
        fps (int): Target frames per second
        background_color (list): RGBA color values for background
        input_text (str): Stores text input from user
        mode (int): Current object manipulation mode (1-4)
        light_pos (list): Position of the light source in 3D space
        camera (Camera): Camera object for view control
    """

    def __init__(self, width, height, title, fullscreen=False, fps=60):
        """
        Initialize the Engine with window and rendering settings.

        Args:
            width (int): Window width in pixels
            height (int): Window height in pixels
            title (str): Window title
            fullscreen (bool, optional): Fullscreen mode flag. Defaults to False.
            fps (int, optional): Target frames per second. Defaults to 60.

        Raises:
            Exception: If GLFW initialization fails
        """
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
        self.mode = 0

        self.light_pos = [2.0, 2.0, 2.0]
        self.angle_x_1 = 0.0
        self.angle_x_2 = 0.0
        self.angle_x_3 = 0.0

        self.angle_y_1 = 0.0
        self.angle_y_2 = 0.0
        self.angle_y_3 = 0.0

        self.angle_z_1 = 0.0
        self.angle_z_2 = 0.0
        self.angle_z_3 = 0.0

        self.y_1 = 0.0
        self.y_2 = 0.0
        self.y_3 = 0.0
        self.x_1 = 0.0
        self.x_2 = 0.0
        self.x_3 = 0.0
        self.z_1 = 0.0
        self.z_2 = 0.0
        self.z_3 = 0.0
        self.scaling_1 = 1.0
        self.scaling_2 = 1.0
        self.scaling_3 = 1.0

        self.camera = Camera(
            position=[0.0, 0.0, 3.0], target=[0.0, 0.0, 0.0], up_vector=[0.0, 1.0, 0.0]
        )

    def initialize(self):
        """
        Initialize the window and OpenGL context.
        
        Sets up the window, enables depth testing, and registers all input callbacks.
        Must be called before starting the main loop.
        """
        self.window = Window(self.width, self.height, self.title, self.fullscreen, None)
        self.window.setup()

        glEnable(GL_DEPTH_TEST)

        glfw.set_key_callback(self.window.getWindow(), self.key_callback)
        glfw.set_mouse_button_callback(
            self.window.getWindow(), self.mouse_button_callback
        )
        glfw.set_cursor_pos_callback(
            self.window.getWindow(), self.cursor_position_callback
        )
        glfw.set_char_callback(self.window.getWindow(), self.text_input_callback)
        glfw.set_scroll_callback(self.window.getWindow(), self.scroll_callback)

    def key_callback(self, window, key, scancode, action, mods):
        """
        Handle keyboard input events.

        Args:
            window: GLFW window instance
            key (int): The keyboard key that was pressed or released
            scancode (int): The system-specific scancode of the key
            action (int): GLFW_PRESS, GLFW_RELEASE or GLFW_REPEAT
            mods (int): Bit field describing which modifier keys were held down
        """
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            self.background_color = [
                random.random(),
                random.random(),
                random.random(),
                1.0,
            ]
        elif key == glfw.KEY_R and action == glfw.PRESS:
            self.background_color = [0.2, 0.2, 0.2, 1.0]
        elif key == glfw.KEY_BACKSPACE and (
            action == glfw.PRESS or action == glfw.REPEAT
        ):
            self.input_text = self.input_text[:-1]

        elif key == glfw.KEY_UP and action == glfw.PRESS:
            if self.mode == 1:
                self.y_1 += 0.1
            elif self.mode == 2:
                self.y_2 += 0.1
            elif self.mode == 3:
                self.y_3 += 0.1
            elif self.mode == 4:
                self.y_4 += 0.1
        elif key == glfw.KEY_DOWN and action == glfw.PRESS:
            if self.mode == 1:
                self.y_1 -= 0.1
            elif self.mode == 2:
                self.y_2 -= 0.1
            elif self.mode == 3:
                self.y_3 -= 0.1
            elif self.mode == 4:
                self.y_4 -= 0.1
        elif key == glfw.KEY_LEFT and action == glfw.PRESS:
            if self.mode == 1:
                self.x_1 -= 0.1
            elif self.mode == 2:
                self.x_2 -= 0.1
            elif self.mode == 3:
                self.x_3 -= 0.1
            elif self.mode == 4:
                self.x_4 -= 0.1
        elif key == glfw.KEY_RIGHT and action == glfw.PRESS:
            if self.mode == 1:
                self.x_1 += 0.1
            elif self.mode == 2:
                self.x_2 += 0.1
            elif self.mode == 3:
                self.x_3 += 0.1
            elif self.mode == 4:
                self.x_4 += 0.1
        elif key == glfw.KEY_EQUAL and action == glfw.PRESS:
            if self.mode == 1:
                self.scaling_1 += 0.1
            elif self.mode == 2:
                self.scaling_2 += 0.1
            elif self.mode == 3:
                self.scaling_3 += 0.1

        elif key == glfw.KEY_MINUS and action == glfw.PRESS:
            if self.mode == 1:
                if self.scaling_1 <= 0.11:
                    self.scaling_1 = 0.1
                else:
                    self.scaling_1 -= 0.1
            elif self.mode == 2:
                if self.scaling_2 <= 0.11:
                    self.scaling_2 = 0.1
                else:
                    self.scaling_2 -= 0.1
            elif self.mode == 3:
                if self.scaling_3 <= 0.11:
                    self.scaling_3 = 0.1
                else:
                    self.scaling_3 -= 0.1
        elif key == glfw.KEY_W and action == glfw.PRESS:
            if self.mode == 1:
                self.angle_x_1 += 1
            elif self.mode == 2:
                self.angle_x_2 += 1
            elif self.mode == 3:
                self.angle_x_3 += 1
        elif key == glfw.KEY_A and action == glfw.PRESS:
            if self.mode == 1:
                self.angle_z_1 += 1
            elif self.mode == 2:
                self.angle_z_2 += 1
            elif self.mode == 3:
                self.angle_z_3 += 1
        elif key == glfw.KEY_D and action == glfw.PRESS:
            if self.mode == 1:
                self.angle_z_1 -= 1
            elif self.mode == 2:
                self.angle_z_2 -= 1
            elif self.mode == 3:
                self.angle_z_3 -= 1
        elif key == glfw.KEY_S and action == glfw.PRESS:
            if self.mode == 1:
                self.angle_x_1 -= 1
            elif self.mode == 2:
                self.angle_x_2 -= 1
            elif self.mode == 3:
                self.angle_x_3 -= 1
        elif key == glfw.KEY_E and action == glfw.PRESS:
            if self.mode == 1:
                self.angle_y_1 -= 1
            elif self.mode == 2:
                self.angle_y_2 -= 1
            elif self.mode == 3:
                self.angle_y_3 -= 1
        elif key == glfw.KEY_Q and action == glfw.PRESS:
            if self.mode == 1:
                self.angle_y_1 += 1
            elif self.mode == 2:
                self.angle_y_2 += 1
            elif self.mode == 3:
                self.angle_y_3 += 1

        elif key == glfw.KEY_J and action == glfw.PRESS:
            self.camera.move([0.0, 0.1, 0.0])
        elif key == glfw.KEY_K and action == glfw.PRESS:
            self.camera.move([0.0, -0.1, 0.0])
        elif key == glfw.KEY_L and action == glfw.PRESS:
            self.camera.move([0.1, 0.0, 0.0])
        elif key == glfw.KEY_N and action == glfw.PRESS:
            self.camera.move([-0.1, 0.0, 0.0])
        elif key == glfw.KEY_M and action == glfw.PRESS:
            self.camera.move([0.0, 0.0, -0.1])
        elif key == glfw.KEY_B and action == glfw.PRESS:
            self.camera.move([0.0, 0.0, 0.1])
        elif key == glfw.KEY_1 and action == glfw.PRESS:
            self.mode = 1
        elif key == glfw.KEY_2 and action == glfw.PRESS:
            self.mode = 2
        elif key == glfw.KEY_3 and action == glfw.PRESS:
            self.mode = 3
        elif key == glfw.KEY_4 and action == glfw.PRESS:
            self.mode = 4

    def mouse_button_callback(self, window, button, action, mods):
        """
        Handle mouse button events.

        Args:
            window: GLFW window instance
            button (int): The mouse button that was pressed or released
            action (int): GLFW_PRESS or GLFW_RELEASE
            mods (int): Bit field describing which modifier keys were held down
        """
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            self.background_color = [
                random.random(),
                random.random(),
                random.random(),
                1.0,
            ]

    def cursor_position_callback(self, window, xpos, ypos):
        """
        Handle mouse cursor movement.

        Args:
            window: GLFW window instance
            xpos (float): New cursor x-coordinate
            ypos (float): New cursor y-coordinate
        """
        self.background_color = [xpos / self.width, ypos / self.height, 0.5, 1.0]

    def scroll_callback(self, window, xoffset, yoffset):
        """
        Handle mouse scroll wheel events.

        Args:
            window: GLFW window instance
            xoffset (float): Scroll offset along the x-axis
            yoffset (float): Scroll offset along the y-axis
        """
        self.background_color = [yoffset / 0.5, yoffset / 1.0, 1, 1.0]

    def text_input_callback(self, window, character):
        """
        Handle text input events.

        Args:
            window: GLFW window instance
            character (int): Unicode codepoint of the character
        """
        self.input_text += chr(character)

    def set_projection(self, fov, aspect, zNear, zFar, type):
        """
        Set the projection matrix for rendering.

        Args:
            fov (float): Field of view in degrees
            aspect (float): Aspect ratio (width/height)
            zNear (float): Near clipping plane distance
            zFar (float): Far clipping plane distance
            type (int): Projection type (1 for perspective, other for orthographic)
        """
        if type == 1:
            self.projection_matrix = glm.perspective(
                glm.radians(fov), aspect, zNear, zFar
            )
        else:
            self.projection_matrix = glm.ortho(-aspect, aspect, -1.0, 1.0, zNear, zFar)

    def main_loop(self):
        """
        Main game loop that handles rendering and updates.
        
        This method:
        - Maintains the target frame rate
        - Updates window title with FPS
        - Handles input processing
        - Creates and renders scene objects
        - Manages window buffer swapping
        - Controls frame timing
        """
        while (
            not glfw.window_should_close(self.window.getWindow())
            and not self.window_should_close
        ):
            width, height = glfw.get_window_size(self.window.getWindow())
            glViewport(0, 0, width, height)
            currentTime = glfw.get_time()
            self.frameCount += 1
            if (currentTime - self.previousTime) >= 1.0:
                glfw.set_window_title(
                    self.window.getWindow(), f"FPS: {self.frameCount}"
                )
                self.frameCount = 0
                self.previousTime = currentTime

            
            if self.input_text == "black":
                self.background_color = [0, 0, 0, 1]

            # self.camera.set_projection(fov=45.0, aspect_ratio=width/height, near=0.1, far=100.0)

            glClearColor(*self.background_color)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # view = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -5.0))
            # self.set_projection(45.0, width / height, 0.1, 100.0, 1)

            

        
            

            view = self.camera.view_matrix
            MVP_half = self.projection_matrix * view

            cube = Cube(vertex_shader_source, fragment_shader_source)
            cube_lamp = LightCube(lamp_vertex_shader, lamp_fragment_shader)
            textured_cube = TexturedCube(
                texture_vertex_shader,
                texture_fragment_shader,
                "textures/wood.png"
            )
            textured_sphere = TexturedSphere(
                texture_vertex_shader,
                texture_fragment_shader,
                "textures/earth.jpg",  
                radius=1.0,
                sectors=32, 
                stacks=16,
            )

            points_fan = [
                0.0, 0.0, 0.0,
                0.5, 0.0, 0.0,
                0.35, 0.35, 0.0,
                0.0, 0.5, 0.0,
                -0.35, 0.35, 0.0,
                -0.5, 0.0, 0.0,
                -0.35, -0.35, 0.0,
                0.0, -0.5, 0.0,
                0.35, -0.35, 0.0,
                0.5, 0.0, 0.0  
            ]

            points_strip = [
                -0.5, -0.5, 0.0,
                -0.5, 0.5, 0.0,
                0.0, -0.5, 0.0,
                0.0, 0.5, 0.0,
                0.5, -0.5, 0.0,
                0.5, 0.5, 0.0
            ]

            triangle_fan = Triangle_fans(points_fan, vertex_shader_source, fragment_shader_source)
            triangle_strip = Triangle_strip(points_strip, vertex_shader_source, fragment_shader_source)

            triangle_fan.translate(-2.0, -2.0)  
            triangle_strip.translate(2.0, -2.0) 

      
            cube.translate(self.x_1, self.y_1)
            cube.rotate(self.angle_x_1, self.angle_y_1, self.angle_z_1)
            cube.scale(self.scaling_1)
            
            textured_cube.translate(self.x_2, self.y_2)
            textured_cube.rotate(self.angle_x_2, self.angle_y_2, self.angle_z_2)
            textured_cube.scale(self.scaling_2)
            
            textured_sphere.translate(self.x_3, self.y_3)
            textured_sphere.rotate(self.angle_x_3, self.angle_y_3, self.angle_z_3)
            textured_sphere.scale(self.scaling_3)

            textured_cube.draw(self.projection_matrix, view, self.camera.get_position(), self.light_pos)
            textured_sphere.draw(self.projection_matrix, view, self.camera.get_position(), self.light_pos)
            cube.draw(self.projection_matrix, view, self.camera.get_position(), self.light_pos)
            cube_lamp.draw(self.projection_matrix, view, self.light_pos)

            triangle_fan.draw(self.projection_matrix, view)
            triangle_strip.draw(self.projection_matrix, view)

            print(self.mode)
            #triangle.draw(self.projection_matrix, view)
            #triangle_fan.draw(self.projection_matrix, view)
            #triangle_strip.draw(self.projection_matrix, view)

            glfw.swap_buffers(self.window.getWindow())
            glfw.poll_events()

            elapsed_time = glfw.get_time() - currentTime
            if elapsed_time < self.frame_duration:
                time.sleep(self.frame_duration - elapsed_time)

    def terminate(self):
        """
        Clean up resources and terminate GLFW.
        Should be called when the application exits.
        """
        glfw.terminate()
