import numpy as np
from objects.GameObject import *
import glm


class UpdataleObject:
    """
    A base class for objects that can be updated each frame.

    This class provides basic update functionality for game objects.

    Attributes:
        update_count (int): Counter tracking number of updates performed
    """

    def __init__(self):
        """Initialize update counter."""
        self.update_count = 0

    def update(self):
        """
        Update the object state.
        Increments the update counter.
        """
        self.update_count += 1
