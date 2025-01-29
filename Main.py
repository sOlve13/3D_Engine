from Engine import Engine
from OpenGL.GL import *
import glm

"""
Main entry point for the OpenGL application.

This module initializes the OpenGL window, sets up the scene objects,
and runs the main rendering loop.

Attributes:
    WINDOW_WIDTH (int): Initial window width in pixels
    WINDOW_HEIGHT (int): Initial window height in pixels
    WINDOW_TITLE (str): Window title text
    
Example:
    Run the application:
        $ python Main.py
"""

def main():
    """
    Initialize and run the main application loop.
    
    Sets up GLFW window, creates scene objects, handles input,
    and manages the render loop.
    """

    engine = Engine(1280, 800, "3D", False, 6000)
    
    engine.initialize()
    

    engine.set_projection(60.0, 1280.0 / 800.0, 0.1, 100.0, 1)
    
    engine.main_loop()
    
    engine.terminate()


if __name__ == "__main__":
    main()
