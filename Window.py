# Window.py

import glfw

class Window:
    def __init__(self, W, H, title, monitor = False, share = False):
        self.W = W
        self.H = H
        self.title = title
        self.monitor = monitor
        self.share = share
        self.window = None

    def setup(self):
        self.window = glfw.create_window(int(self.W), int(self.H), self.title, self.monitor, self.share)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window could not be created!")
        glfw.make_context_current(self.window)

    def getWindow(self):
        return self.window
