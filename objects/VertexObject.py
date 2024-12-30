import glfw
from OpenGL.GL import *
import random
from Window import Window
import glm
import time
import numpy as np


class Vertex:
    def __init__(self, position, color = (1.0, 1.0, 1.0), normal = (0.0, 0.0, 0.0)):
        self.position = position
        self.color = color
        self.normal = normal
    
    def translate(self, x, y, z):
        self.position = (
                self.position[0] + x,
                self.position[1] + y,
                self.position[2] + z
                )
    def scale(self, mp):
        self.position = (
                self.position[0] * mp,
                self.position[1] * mp,
                self.position[2] * mp
                )