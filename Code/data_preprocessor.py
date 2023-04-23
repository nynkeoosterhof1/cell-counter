"""
Preprocess all input data.

Classes: 
    DataProprocessor

Functions:
    preprocess_images(self, preprocessing_steps=['clahe_per_slice', 
                                                 'median'],
                      clipLimit=0.07, nbins=127, footprint=np.ones((5,5)))
    make_composites(self)
    trim_images(self)
    get_slice_info(self)
"""

from msilib.schema import File
from file_manager import FileManager
from sample_preprocessor import SamplePreprocessor
import numpy as np

class DataPreprocessor(FileManager):
    """
    Data preprocessor. Inherits from FileManager.

    Attributes:
        See FileManager.
        folder_path : str
            Path of data folder.
        sample_folders : list of strings
            List containing all paths of sample folders (subfolders of 
            data folder).
        channels_to_preprocess : list of strings
            List of channel names to preprocess.

    Methods:
        preprocess_images(self, preprocessing_steps=['clahe_per_slice',
                                                     'median'],
                          clipLimit=0.07, nbins=127, footprint=np.ones((5,5))):
            Run preprocessing operations. 
        make_composites(self):
            Create composite image.
        trim_images(self):
            Trim z-stack.
        get_slice_info(self):
            Read z-slice information.
    """

    def __init__(self, path_folder, channels_to_preprocess = ['Blue']):
        """
        Construct all necessary attributes for the DataProprocessor 
        object.
        Calls __init__() from FileManager class.

        Arguments:
            path_folder : str
                Path in which to find the data file(s).
            channels_to_preprocess : list of strings
                Name of channel(s) to preprocess. Default is Blue.
        """
        super().__init__(path_folder)
        self.folder_path = path_folder
        self.sample_folders = self.get_subfolders(self.folder_path)
        self.channels_to_preprocess = channels_to_preprocess
    
    def preprocess_images(self, preprocessing_steps=['clahe_per_slice', 
                                                     'median'], 
                          clipLimit=0.07, nbins=127, footprint=np.ones((5,5))):
        """
        Run preprocessing on each sample with SamplePreprocessor.
        
        Arguments:
            preprocessing_steps : list of strings
                Choice of preprocessing method(s). Default is both CLAHE
                and a Median filter.
            clipLimit : float
                Clip limit for CLAHE. Default is 0.07.
            nbins : int
                Number of bins used in CLAHE. Default is 127.
            footprint : numerical array filled with ones
                Array of ones to use as the Median filter. Default is a
                5x5 array.
        """
        for sample_folder in self.sample_folders:
            sample_preprocessor = SamplePreprocessor(sample_folder, 
                                                     self.channels_to_preprocess)
            sample_preprocessor.preprocess_sample(preprocessing_steps=preprocessing_steps, 
                                                  clipLimit=clipLimit, nbins=nbins, 
                                                  footprint=footprint)
    
    def make_composites(self):
        """Make composites of all channels using SamplePreprocessor."""
        for sample_folder in self.sample_folders:
            sample_preprocessor = SamplePreprocessor(sample_folder)
            sample_preprocessor.make_composite()

    def trim_images(self):
        """Trim images to desired length using SmaplePreprocessor."""
        for sample_folder in self.sample_folders:
            sample_preprocessor = SamplePreprocessor(sample_folder)
            sample_preprocessor.trim_images_sample(sample_folder)

    def get_slice_info(self):
        """Read z-slice information using SamplePreprocessor."""
        for sample_folder in self.sample_folders:
            sample_preprocessor = SamplePreprocessor(sample_folder)
            sample_preprocessor.save_slice_info()