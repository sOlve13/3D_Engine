from Engine import Engine
from OpenGL.GL import *
import numpy as np


def main():
    engine = Engine(1280, 800, "3D", False, 60)
    engine.initialize()
    engine.set_projection(60.0, 1280.0 / 800.0, 0.1, 100.0, 1)
    engine.main_loop()
    engine.terminate()


if __name__ == "__main__":
    main()
