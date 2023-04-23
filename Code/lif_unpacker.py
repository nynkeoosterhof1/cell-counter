"""
Unpack multi-channel .lif files into single-channel images.

Classes:
    LifUnpacker

Functions:
    get_images_lif_file(self, reader)   
    save_image_as_tiff(self, image_path, image)
    unpack_images(self)
    unpack_image(self, image)
    get_new_folder_names(self, channels)
"""

import read_lif
from skimage.io import imsave
from skimage.util import img_as_uint
from file_manager import FileManager

class LifUnpacker(FileManager):
    """
    Lif file unpacker. Inherits from FileManager.

    Attributes:
        See FileManager.
        folder_path : str
            Path of folder. 
        lif_path : str
            Path of .lif file.
        file_name : str
            Name of .lif file.
        reader : ?
            Reader object for .lif files.
        images : numpy array?
            Images found in the .lif file.
        output_folder : ?
            Folder in which to store unpacked single-channel images?
        z_stack : ?
            ? 

    Methods:
        get_images_lif_file(self, reader):
            Read the images stored in the .lif file.  
        save_image_as_tiff(self, image_path, image):
            Save unpacked, single-channel image as a .tiff file.
        unpack_images(self):
            Call unpack_image(self, image) for each image in the .lif 
            file.
        unpack_image(self, image):
            Return single-channel images for each image channel.
        get_new_folder_names(self, channels):
            Return folder names for each image channel.
    """

    def __init__(self, folder_path, file_name, only_z_stack=True):
        """
        Construct all necessary attributes for the LifUnpacker object.
        Extends __init__() from FileManager class.

        Arguments:
            folder_path : str
                Path in which to find the .lif file(s).
            file_name : str
                Name of the .lif file.
            only_z_stack : boolean
                ??. Default is True.
        """
        super().__init__(folder_path)
        
        self.folder_path = folder_path
        self.lif_path = folder_path + file_name
        self.file_name = file_name.split('.')[0]
        self.reader = read_lif.Reader(self.lif_path)
        self.images = self.get_images_lif_file(self.reader) 
        print(self.images)
        self.output_folder = self.make_new_folder(self.folder_path, 
                                                  self.file_name) 
        self.z_stack = only_z_stack

    def get_images_lif_file(self, reader):
        """Return the images loaded from a .lif file as arrays."""
        return reader.getSeries() 

    def save_image_as_tiff(self, image_path, image):
        """Save a single-channel image as a .tiff file."""
        imsave(image_path, img_as_uint(image))
    
    def unpack_images(self):
        """Call unpack_image() for each .lif file in the folder."""
        for image in self.images:
            self.unpack_image(image)

    def unpack_image(self, image):
        """
        Separate a multi-channel .lif file into its separate channels 
        and save each single-channel image into a channel-specific 
        folder.

        Arguments:
            image : ?
                .lif file to be unpacked.
        """
        image_name = image.getName()
        channels = image.getChannels()
        folder_names = self.get_new_folder_names(channels)
        
        if image.hasZ():
            for channel in range(len(channels)):
                new_path = self.make_new_folder(self.output_folder, 
                                                folder_names[channel])
                z_stack = image.getFrame(channel=channel)
                image_path = new_path + image_name + '.tif'
                self.save_image_as_tiff(image_path, z_stack)

    def get_new_folder_names(self, channels):
        """
        Return folder names for the unpacked single-channel images.
        Folders are named according to the name of the LUT used during
        image acquisition. If the same LUT was used twice, the name is
        set to <LUTName>_2.

        Arguments:
            channels : (type)
                single-channels within a multi-channel image.
        """
        folder_names = []
        for c in channels:
            channel_name = c.getAttribute('LUTName')
            if channel_name in folder_names:
                folder_names.append(channel_name + '_2')
            else:
                folder_names.append(channel_name)
        return folder_names