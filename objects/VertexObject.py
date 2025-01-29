import glfw
from OpenGL.GL import *
import random
from Window import Window
import glm
import time
import numpy as np


class Vertex:
    """
    A class representing a vertex with position, color and normal attributes.

    This class handles individual vertex data and transformations.

    Attributes:
        position (tuple): XYZ coordinates of the vertex
        color (tuple): RGB color values, defaults to white (1.0, 1.0, 1.0)
        normal (tuple): Normal vector, defaults to (0.0, 0.0, 0.0)

    Methods:
        translate(x, y, z): Translates the vertex by given offsets
        scale(mp): Scales vertex position by multiplication factor
    """
    def __init__(self, position, color = (1.0, 1.0, 1.0), normal = (0.0, 0.0, 0.0)):
        """
        Initialize a Vertex object.

        Args:
            position (tuple): XYZ coordinates of the vertex
            color (tuple): RGB color values, defaults to white
            normal (tuple): Normal vector, defaults to zero vector
        """
        self.position = position
        self.color = color
        self.normal = normal
    
    def translate(self, x, y, z):
        """
        Translate the vertex position.

        Args:
            x (float): Translation along X axis
            y (float): Translation along Y axis
            z (float): Translation along Z axis
        """
        self.position = (
                self.position[0] + x,
                self.position[1] + y,
                self.position[2] + z
                )
    def scale(self, mp):
        """
        Scale the vertex position.

        Args:
            mp (float): Scale multiplier to apply to position
        """
        self.position = (
                self.position[0] * mp,
                self.position[1] * mp,
                self.position[2] * mp
                )