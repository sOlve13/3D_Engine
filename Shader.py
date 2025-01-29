"""
Shader program management class.

Handles compilation and linking of vertex and fragment shaders,
and provides utilities for setting uniform variables.

Attributes:
    vertex_source (str): Vertex shader source code
    fragment_source (str): Fragment shader source code
    program_id (int): OpenGL shader program ID
"""

class Shader:
    def __init__(self, vertex_source, fragment_source):
        """
        Create and compile shader program.

        Args:
            vertex_source (str): Vertex shader source code
            fragment_source (str): Fragment shader source code
            
        Raises:
            Exception: If shader compilation or program linking fails
        """
        # ... existing code ...

    def use(self):
        """Activate this shader program for rendering."""
        # ... existing code ...

    def set_bool(self, name, value):
        """
        Set boolean uniform variable.

        Args:
            name (str): Uniform variable name
            value (bool): Value to set
        """
        # ... existing code ...

    def set_int(self, name, value):
        """
        Set integer uniform variable.

        Args:
            name (str): Uniform variable name
            value (int): Value to set
        """
        # ... existing code ...

    def set_float(self, name, value):
        """
        Set float uniform variable.

        Args:
            name (str): Uniform variable name
            value (float): Value to set
        """
        # ... existing code ...

    def set_vec2(self, name, value):
        """
        Set vec2 uniform variable.

        Args:
            name (str): Uniform variable name
            value (tuple): Two float values (x, y)
        """
        # ... existing code ...

    def set_vec3(self, name, value):
        """
        Set vec3 uniform variable.

        Args:
            name (str): Uniform variable name
            value (tuple): Three float values (x, y, z)
        """
        # ... existing code ...

    def set_vec4(self, name, value):
        """
        Set vec4 uniform variable.

        Args:
            name (str): Uniform variable name
            value (tuple): Four float values (x, y, z, w)
        """
        # ... existing code ...

    def set_mat2(self, name, mat):
        """
        Set mat2 uniform variable.

        Args:
            name (str): Uniform variable name
            mat (numpy.ndarray): 2x2 matrix
        """
        # ... existing code ...

    def set_mat3(self, name, mat):
        """
        Set mat3 uniform variable.

        Args:
            name (str): Uniform variable name
            mat (numpy.ndarray): 3x3 matrix
        """
        # ... existing code ...

    def set_mat4(self, name, mat):
        """
        Set mat4 uniform variable.

        Args:
            name (str): Uniform variable name
            mat (numpy.ndarray): 4x4 matrix
        """
        # ... existing code ...

    def __del__(self):
        """Clean up shader program."""
        # ... existing code ... 