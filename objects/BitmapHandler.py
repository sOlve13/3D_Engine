from PIL import Image
import numpy as np
from OpenGL.GL import *

"""
A class for handling texture loading and management in OpenGL.

This class provides functionality for loading, binding, and cleaning up texture resources.

Attributes:
    textures (dict): Dictionary mapping texture file paths to OpenGL texture IDs
"""

class BitmapHandler:
    def __init__(self):
        """Initialize empty texture dictionary."""
        self.textures = {}

    def load_texture(self, file_path):
        """
        Load a texture from an image file.

        Args:
            file_path (str): Path to the image file

        Returns:
            int: OpenGL texture ID if successful, None if failed

        Note:
            Automatically converts non-RGBA images to RGBA format
            Caches textures to avoid reloading the same texture
        """
        if file_path in self.textures:
            return self.textures[file_path]

        try:
            image = Image.open(file_path)
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            img_data = np.array(image)

            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGBA,
                image.width,
                image.height,
                0,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                img_data
            )

            glGenerateMipmap(GL_TEXTURE_2D)

            self.textures[file_path] = texture_id

            image.close()
            
            return texture_id

        except Exception as e:
            print(f"Error loading texture {file_path}: {str(e)}")
            return None

    def bind_texture(self, texture_id, texture_unit=GL_TEXTURE0):
        """
        Bind a texture to a texture unit.

        Args:
            texture_id (int): OpenGL texture ID
            texture_unit (int): OpenGL texture unit to bind to (default: GL_TEXTURE0)
        """
        glActiveTexture(texture_unit)
        glBindTexture(GL_TEXTURE_2D, texture_id)

    def delete_texture(self, texture_id):
        """
        Delete a texture from OpenGL and remove it from cache.

        Args:
            texture_id (int): OpenGL texture ID to delete
        """
        if texture_id:
            glDeleteTextures(1, [texture_id])
            for path, tid in list(self.textures.items()):
                if tid == texture_id:
                    del self.textures[path]

    def cleanup(self):
        """Delete all textures and clear the texture cache."""
        for texture_id in self.textures.values():
            glDeleteTextures(1, [texture_id])
        self.textures.clear()

    def __del__(self):
        """Ensure all textures are properly cleaned up on deletion."""
        self.cleanup()
