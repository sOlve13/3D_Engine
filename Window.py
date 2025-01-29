# Window.py

import glfw

"""
Window management class for OpenGL applications.

Handles window creation, input processing, and basic OpenGL context setup.

Attributes:
    width (int): Window width in pixels
    height (int): Window height in pixels
    title (str): Window title
    window (GLFWwindow): GLFW window handle
"""

class Window:
    """
    A class that handles window creation and management using GLFW.
    """
    def __init__(self, W, H, title, monitor=False, share=False):
        """
        Initialize window parameters.
        
        Args:
            W (int): Window width
            H (int): Window height
            title (str): Window title
            monitor (bool): If True, create fullscreen window
            share (bool): Share resources with another window context
            
        Raises:
            RuntimeError: If GLFW initialization fails
        """
        self.W = W
        self.H = H
        self.title = title
        self.monitor = monitor
        self.share = share
        self.window = None

    def setup(self):
        """
        Create and setup the GLFW window.
        
        If monitor=True, creates a fullscreen window at monitor's native resolution.
        Otherwise, creates a windowed mode window with specified dimensions.
        
        Raises:
            Exception: If window creation fails
        """
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
            # Create windowed mode window
            self.window = glfw.create_window(int(self.W), int(self.H), self.title, None, self.share)
            
        # Check if window creation was successful
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window could not be created!")
            
        # Set the current OpenGL context
        glfw.make_context_current(self.window)

    def getWindow(self):
        """
        Returns the GLFW window object.
        
        Returns:
            GLFWwindow: The created window object
        """
        return self.window

    def should_close(self):
        """
        Check if window should close.

        Returns:
            bool: True if window should close, False otherwise
        """
        return glfw.window_should_close(self.window)

    def swap_buffers(self):
        """Update window by swapping front and back buffers."""
        glfw.swap_buffers(self.window)

    def process_input(self):
        """
        Process keyboard input.
        
        Handles:
        - Window close on ESC
        - Camera movement on WASD
        - Other key bindings
        """
        glfw.poll_events()

    def __del__(self):
        """Clean up GLFW resources."""
        glfw.destroy_window(self.window)
