import numpy as np
from objects.GameObject import *
import glm


class TransformableObject:
    """
    A base class for objects that can be transformed in 3D space.

    Provides methods for scaling, rotation and translation transformations.

    Attributes:
        trans (glm.mat4): Transformation matrix storing the object's transformations

    Methods:
        scale(scale): Scales the object uniformly
        rotate(angle_x, angle_y, angle_z): Rotates the object around each axis
        translate(x, y): Translates the object in XY plane
    """

    def __init__(self):
        """Initialize transformation matrix to identity."""
        self.trans = glm.mat4(1.0)

    def scale(self, scale):
        """
        Scale the object uniformly.

        Args:
            scale (float): Scale factor to apply in all dimensions
        """
        scale_matrix = glm.scale(glm.mat4(1.0), glm.vec3(scale, scale, scale))
        self.trans *= scale_matrix

    def rotate(self, angle_x, angle_y, angle_z):
        """
        Rotate the object around all axes.

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
        Translate the object in XY plane.

        Args:
            x (float): Translation along X axis
            y (float): Translation along Y axis
        """
        self.trans = glm.translate(self.trans, glm.vec3(x, y, 0))
