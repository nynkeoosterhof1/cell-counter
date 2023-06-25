from data_intensity_counter import DataIntensityCounter
from image_unpacker import ImageUnpacker
from data_preprocessor import DataPreprocessor
from data_cell_counter import DataCellCounter
from data_intensity_counter import DataIntensityCounter
import numpy as np


###############  Unpacking of Images  ###########################

RAW_DATA_FOLDER = 'ADD PATH'

##############  Image preprocessing  ############################

CHANNELS_TO_PREPROCESS = ['Blue']
PREPROCESSING_STEPS = ['clahe_per_slice', 'median']
CLIP_LIMIT = 0.07 # For clahe histogram equalization
NBINS = 127 # For clahe histogram equalization
FOOTPRINT = np.ones((5,5)) # For median filter


################# Data analysis settings (masks) ################


NAME_FOLDER_2D_LABELMAPS = 'labelmaps_2D'
NAME_FOLDER_3D_LABELMAPS = 'labelmaps_3D'
NAME_FOLDER_MASKS_TELENCEPHALON = 'labelmasks_tel'
NAME_FOLDER_MASKS_NEURONS = 'labelmaps_neur'



################ Data analysis settings (intensity) #############


NAME_RESULTS_FILE = 'results.json'
NAME_LABELMAP_FOLDER = 'labels_total'
CHANNELS_TO_USE = ['Green', 'Red']
MODE = 'mean'
CHANNEL_THRESHOLDS_MEAN = [70, 40]
CHANNEL_THRESHOLDS_MAX = [100, 100]
PREPROCESSED = True


################# Unpack images #################################


unpack = ImageUnpacker(RAW_DATA_FOLDER)
unpack.unpack_images()
dataset_folders = unpack.get_subfolders(unpack.folder)
channels = unpack.get_subfolders(dataset_folders[0])


################ Preprocess images ##############################


data_preprocessor = DataPreprocessor(RAW_DATA_FOLDER, CHANNELS_TO_PREPROCESS)
data_preprocessor.make_composites()
data_preprocessor.preprocess_images(preprocessing_steps=PREPROCESSING_STEPS, clipLimit=CLIP_LIMIT, nbins=NBINS, footprint=FOOTPRINT)


##### Get slice info (in case you want to remove some z-slices) ##

data_preprocessor.get_slice_info()
# Manually check which slices to keep for further analysis
data_preprocessor.trim_images()


################### Cellpose ####################################


# Run cellpose by yourself and put the labelmaps in the appropriate folders and 
# add the folder name in the constants specified above


#################### Draw masks ##################################


# Use napari to draw the masks over the areas you want to analyze and put
# the masks in the constants specified above


#################### Count cells #################################

counter = DataCellCounter(RAW_DATA_FOLDER, 'labelmaps_2D', 'labelmaps_3D', 'labelmasks_tel', 'labelmasks_neur')
counter.analyze_data()


################### Count cells based on intensity values #########

intensity_counter = DataIntensityCounter(RAW_DATA_FOLDER, NAME_RESULTS_FILE, NAME_LABELMAP_FOLDER, CHANNELS_TO_USE, MODE, CHANNEL_THRESHOLDS_MEAN, CHANNEL_THRESHOLDS_MAX, PREPROCESSED)
intensity_counter.count_cells()
intensity_counter.save_results()









