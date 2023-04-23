"""
Preprocess all datasets in the data.

Classes:
    SamplePreprocessor

Functions:
    get_channels_to_preprocess(self, channels_to_preprocess)
    get_common_files_in_subfolders(self)
    trim_images_in_subfolder(self, folder_path, slice_info)
    retrieve_slice_info(self)
    save_slice_info(self)
    make_composite(self)

"""

from file_manager import FileManager
from single_channel_preprocessor import SingleChannelPreprocessor
import os
import numpy as np
from skimage.io import imread, imsave
from skimage.util import img_as_uint

class SamplePreprocessor(FileManager):
    """
    Sample Preprocessor. Inherits from FileManager.

    Attributes:
        See FileManager.
        folder_path : str
            Path in which to find a dataset.
        subfolders : list of strings
            List containing all paths of single channel folders 
            (subfolders of sample folder).
        channels_to_preprocess : list of strings
            List of channel names to preprocess.
        common_files : x
            x
        composite_folder : x path? folder?
            Folder in which to store composite images.
    
    Methods:
        get_channels_to_preprocess(self, channels_to_preprocess):
            x
        get_common_files_in_subfolders(self):
            ?
        trim_images_in_subfolder(self, folder_path, slice_info):
            x
        retrieve_slice_info(self):
            x
        save_slice_info(self): 
            x
        make_composite(self):
            x
    """

    def __init__(self, path_folder, channels_to_preprocess=['Blue']):
        """
        Construct all necessary attributes for the SamplePreprocessor 
        object.
        Calls __init__() from FileManager class.

        Arguments:
            path_folder : str
                Path in which to find the sample file(s).
            channels_to_preprocess : list of strings
                Name of channel(s) to preprocess. Default is Blue.
        """
        super().__init__(path_folder)
        self.folder_path = path_folder
        self.subfolders = self.get_subfolders(self.folder_path)
        self.channels_to_preprocess = self.get_channels_to_preprocess(channels_to_preprocess)
        self.common_files = self.get_common_files_in_subfolders()
        self.composite_folder = self.make_new_folder(self.folder_path, 
                                                     'composite')
        

    def get_channels_to_preprocess(self, channels_to_preprocess):
        """Return list containing each channel to preprocess."""
        channels = []
        for channel in channels_to_preprocess:
            channels.append(channel + '/')
        return channels


    def get_common_files_in_subfolders(self):
        """?"""
        file_lists = []
        for subfolder in self.subfolders:
            file_lists.append(os.listdir(subfolder))
        return list(set.intersection(*[set(list) for list in file_lists]))


    def trim_images_in_subfolder(self, folder_path, slice_info):
        """
        Trim z-stacks for all image files within a dataset.
        For each image file x?

        Arguments:
            folder_path : str
                Path to ?
            slice_info : ?
                ?
        """
        files_in_folder = os.listdir(folder_path)
        for file in files_in_folder:
            if len(file.split('.')) == 2:
                img = imread(folder_path + file)
                start = slice_info[file]['start']
                end = slice_info[file]['end']

                if len(img.shape) == 3:
                    imsave(folder_path + file, 
                           img_as_uint(img[start-1:end,:,:]))
                elif len(img.shape) == 4:
                    imsave(folder_path + file, 
                           img_as_uint(img[start-1:end,:,:,:]))

    
    def retrieve_slice_info(self):
        return self.txt_to_dictionary()


    def save_slice_info(self):
        slice_info = {}
        for file in self.common_files:
            img = imread(self.subfolders[0] + file)
            slice_info[file] = {'start': 1, 'end': img.shape[0]}
        self.save_dict_to_txt(slice_info)
        return slice_info

    
    def make_composite(self):
        images_to_stack = []
        for file in self.common_files:
            if len(file.split('.')) == 2:
                for folder in self.subfolders:
                    img = imread(folder + file)
                    images_to_stack.append(img)
                
                composite = img_as_uint(np.stack(images_to_stack, axis=1))
                imsave(self.composite_folder + file, composite, imagej=True)
                images_to_stack = []
        pass


    def preprocess_sample(self, preprocessing_steps=['clahe_per_slice', 
                                                     'median'], 
                          clipLimit=0.07, nbins=127, footprint=np.ones((5,5))):
        for channel in self.channels_to_preprocess:
            preprocessor = SingleChannelPreprocessor(self.folder_path + channel)
            preprocessor.preprocess_images(preprocessing_steps=preprocessing_steps, 
                                           clipLimit=clipLimit, nbins=nbins, 
                                           footprint=footprint)


    def trim_images_sample(self, folder_path):
        subfolders = self.get_subfolders(folder_path)
        slice_info = self.retrieve_slice_info()

        for folder in subfolders:
            self.trim_images_in_subfolder(folder, slice_info)

            subsubfolders = self.get_subfolders(folder)
            for subfolder in subsubfolders:
                self.trim_images_in_subfolder(subfolder, slice_info)
