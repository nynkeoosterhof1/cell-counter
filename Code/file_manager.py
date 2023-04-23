"""
Collection of access, reading, and writing methods to manage files used
and/or made during the analysis pipeline.

Classes:
    FileManager

Functions:
    get_lif_files(self)
    make_new_folder(self, path, folder_name)   
    has_lifs(self)
    get_subfolders(self, path)
    save_dict_to_txt(self, slice_dictionary)
    txt_to_dictionary(self)
    get_folder_name(self, folder_path)
    remove_files(self, path)
    open_json(self, file_name)
"""

import os
import glob
import json
from statistics import mode

class FileManager():
    """
    File manager for files added, read, written, or removed during the
    execution of the analysis pipeline.

    Attributes:
        folder : str
            Name/path of the folder in which to search for a file.
        has_lif : boolean
            Whether the folder contains a .lif file or not.
    
    Methods:
        get_lif_files(self):
            Get the names of all .lif files in a folder.
        make_new_folder(self, path, folder_name): 
            Create a new folder. 
        has_lifs(self):
            Check if there are .lif files in a folder.
        get_subfolders(self, path):
            Get all subfolders within a folder.
        save_dict_to_txt(self, slice_dictionary):
            Create a dictionary .txt file with z-stack dimensions.
        txt_to_dictionary(self):
            Read z-stack information from dictionary .txt file.
        get_folder_name(self, folder_path):
            Get the name of a folder.
        remove_files(self, path):
            Remove all files in a folder.
        open_json(self, file_name):
            Read out information from .json file.
    """

    def __init__(self, path_folder):
        """
        Construct all necessary attributes for the FileManager object.

        Arguments:
            path_folder : str
                Path in which to find the .lif file(s).
        """
        self.folder = path_folder
        self.has_lif = self.has_lifs()
        # TODO do we not also need to initiate .lif_files to be an empty list?
        self.lif_files = [] #new 
        
    def get_lif_files(self):
        """
        Retrieve the names and paths of all .lif files in a folder and
        adds them to a list of .lif files.
        """
        for name in glob.glob(self.folder + '*.lif'):
            file_path = self.folder + os.path.basename(name)
            self.lif_files.append(file_path)

    def make_new_folder(self, path, folder_name):
        """Create a new folder."""
        if not os.path.exists(path + folder_name):
            os.makedirs(path + folder_name, exist_ok=True)
        return path + folder_name + '/'

    def has_lifs(self):
        """Check if the folder contains a .lif file."""
        for file in os.listdir(self.folder):
            if file.endswith('.lif'):
                return True
        return False

    def get_subfolders(self, path):
        """Return a list of all subfolders within a folder."""
        return [path + subfolder + '/' for subfolder in os.listdir(path) if os.path.isdir(os.path.join(path, subfolder))]

    def save_dict_to_txt(self, slice_dictionary):
        """
        Create a new .txt file and fill it with the name of each 
        image file and the start and end points of the z-stack.

        Arguments:
            slice_dictionary : dictionary
                Key:value pairs containing the start and end point of
                each image in a folder.
        """
        with open(self.folder + "slice_dictionary.txt", mode='a') as file:
            for key in slice_dictionary.keys():
                file_name = key
                start = str(slice_dictionary[key]['start'])
                end = str(slice_dictionary[key]['end'])
                file.write(f'{file_name} {start} {end} \n')

    def txt_to_dictionary(self):
        """
        Return z-stack information in a dictionary as read from the 
        slice_dictionary.txt file.
        For each line in slice_dictionary.txt, split the line by empty 
        spaces and save the information for the start and end points of
        each image in a dictionary.
        """
        dictionary = {}
        with open(self.folder + 'slice_dictionary.txt', mode='r') as file:
            elements = file.readlines()
        
        for element in elements:
            el = element.split(' ')
            dictionary[el[0]] = {'start': int(el[1]), 'end': int(el[2])}
        return dictionary

    def get_folder_name(self, folder_path):
        """Return the name of a folder without the rest of the path."""
        return folder_path.split('/')[-2]

    def remove_files(self, path):
        """Remove all files in a folder.""" 
        # TODO as far as I can tell, this function is never actually used - should it be deleted?
        files = glob.glob(path + '*')
        for f in files:
            os.remove(f)

    def open_json(self, file_name):
        """Read out results from .json file.""" 
        with open(self.folder + file_name, mode='r') as f:
            results = json.load(f)
        return results