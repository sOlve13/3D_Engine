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
        #rewiew later !!!!!!!!!!!
        if self.monitor: 
            # Get the primary monitor and its video mode
            primary_monitor = glfw.get_primary_monitor()
            video_mode = glfw.get_video_mode(primary_monitor)
            
            # Adjust the resolution to match the monitor's native resolution
            self.W, self.H = video_mode.size.width, video_mode.size.height

            self.window = glfw.create_window(
                int(self.W), int(self.H), 
                self.title, 
                primary_monitor, 
                self.share
            )
        else: 
            self.window = glfw.create_window(int(self.W), int(self.H), self.title, None,  self.share)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window could not be created!")
        glfw.make_context_current(self.window)

    def getWindow(self):
        return self.window
