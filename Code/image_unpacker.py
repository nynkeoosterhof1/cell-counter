"""
Unpack image files into single-channel images. Currently only works
with .lif files; functionality could be extended to include other image
formats.

Classes:
    ImageUnpacker

Functions:
    unpack_images(self)   
    unpack_lifs(self)
"""

import os
from file_manager import FileManager
from lif_unpacker import LifUnpacker

class ImageUnpacker(FileManager):
    """
    Image file unpacker. Inherits from FileManager.

    Attributes:
        See FileManager.

    Methods:
        unpack_images(self):
            Call relevant unpack method depending on image format.  
        unpack_lifs(self):
            Unpack .lif file(s) using LifUnpacker.
    """

    def __init__(self, folder_path):
        """
        Construct all necessary attributes for the ImageUnpacker object.
        Calls __init__() from FileManager class.

        Arguments:
            folder_path : str
                Path in which to find the image file(s).
        """
        super().__init__(folder_path)

    def unpack_images(self):
        """Check image format and call corresponding unpack method."""
        if self.has_lif:
            self.unpack_lifs()

    def unpack_lifs(self):
        """Unpack .lif file(s) using LifUnpacker."""
        lifs = [file for file in os.listdir(self.folder) if file.endswith('.lif')]
        for lif in lifs:
            file = LifUnpacker(self.folder, lif)
            file.unpack_images()