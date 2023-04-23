from file_manager import FileManager
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imsave
from skimage.measure import regionprops
from skimage.util import img_as_uint, img_as_ubyte
import pandas as pd
import glob
import os


# PATH_LABELMAP_2D = 'F:/Microscopy/Zeiss780/20210803_staging_GBS/ImagesForQuantification/Nuclei/2D_labelmaps/22hpf_fish3_nuclei_z1-30_2DMask.tif'
# PATH_LABELMAP_3D = 'F:/Microscopy/Zeiss780/20210803_staging_GBS/ImagesForQuantification/Nuclei/3D_labelmaps/22hpf_fish3_nuclei_z1-30_3DMask.tif'
# PATH_LABELMASK_TEL = 'F:/Microscopy/Zeiss780/20210803_staging_GBS/ImagesForQuantification/Neurons/masks_telencephalon/22hpf_fish3_tel_z1-30.tif'
# PATH_LABELMASK_NEUR = 'F:/Microscopy/Zeiss780/20210803_staging_GBS/ImagesForQuantification/Neurons/Masks_neurons/22hpf_fish3_neurons_z1-30.tif'

# labelmap_2D = img_as_uint(imread(PATH_LABELMAP_2D))
# labelmap_3D = img_as_uint(imread(PATH_LABELMAP_3D))
# labelmask_tel = imread(PATH_LABELMASK_TEL)
# labelmask_neur = imread(PATH_LABELMASK_NEUR)


class CellCounter(FileManager):

    def __init__(self, path_folder, image_name, labelmap_2D, labelmap_3D, mask_tel, mask_cell, threshold_ratio = 0.8, threshold_size = 300):
        super().__init__(path_folder)
        self.labelmap_2D = labelmap_2D
        self.labelmap_3D = labelmap_3D
        self.mask_tel = self.make_binary(mask_tel)
        self.mask_cell = self.make_binary(mask_cell)
        self.threshold_ratio = threshold_ratio
        self.threshold_size = threshold_size
        self.image_name = image_name
        self.result = {'labels_total': [], 'labels_neurons': [], 'labels_progenitors': [], 'total_count': 0, 'neuron_count': 0, 'progenitor_count': 0}


    def make_binary(self, mask):
        bin_mask = np.zeros(mask.shape)
        bin_mask[mask > 0] = 1
        return bin_mask
        

    def apply_mask(self, labelmap, mask):
        return labelmap * mask
    

    def get_regionProps(self, labelmap):
        return regionprops(labelmap.astype(dtype=np.uint16))


    def remove_partial_nuclei(self, props_masked, props_all, threshold_ratio, threshold_size):
        labels = []
        for prop in props_masked:
            for prop_a in props_all:
                if prop_a['label'] == prop['label']:
                    if ((prop['area']/prop_a['area']) > threshold_ratio) and (prop['area'] > threshold_size):
                        labels.append(prop['label'])
        return labels

    
    def generate_nuclear_mask_2D(self, masked_labelmap):
        nuclear_mask = np.zeros(masked_labelmap.shape)
        for i in range(masked_labelmap.shape[0]):
            regionprops_masked_labels = regionprops(masked_labelmap[i,:,:].astype(dtype=np.uint16))
            regionprops_all_labels = regionprops(self.labelmap_2D[i,:,:].astype(dtype=np.uint16))
            labels = self.remove_partial_nuclei(regionprops_masked_labels, regionprops_all_labels, self.threshold_ratio, self.threshold_size)
            for label in labels:
                nuclear_mask[i,:,:][masked_labelmap[i,:,:] == label] = label
        return nuclear_mask


    def get_total_labels(self):
        labels = []
        masked_2D_labelmap = self.apply_mask(self.labelmap_2D, self.mask_tel)
        self.nuclear_mask = self.generate_nuclear_mask_2D(masked_2D_labelmap)
        bin_nuclear_mask = self.make_binary(self.nuclear_mask)
        self.labelmap_3D = self.apply_mask(self.labelmap_3D, bin_nuclear_mask)
        properties_3D_labelmap = self.get_regionProps(self.labelmap_3D)

        for prop in properties_3D_labelmap:
            labels.append(prop['label'])
        
        self.result['labels_total'] = labels
        self.make_new_folder(self.folder, 'labels_total')
        imsave(self.folder + 'labels_total/' + self.image_name, self.labelmap_3D.astype(dtype=np.uint16))


    def generate_labelmap_from_labels(self, labels, template_labelmap):
        new_labelmap = np.zeros(template_labelmap.shape)
        for label in labels:
            new_labelmap[template_labelmap == label] = label
        return new_labelmap


    def get_neuronal_counts(self):
        labels = []
        masked_2D_labelmap = self.apply_mask(self.nuclear_mask, self.mask_cell)
        nuclear_mask_neurons = self.generate_nuclear_mask_2D(masked_2D_labelmap)
        bin_nuclear_mask_neurons = self.make_binary(nuclear_mask_neurons)

        # labelmap_3D = self.generate_labelmap_from_labels(self.result['labels_total'], self.labelmap_3D)
        masked_3D_labelmap = self.apply_mask(self.labelmap_3D, bin_nuclear_mask_neurons)
        properties_3D_labelmap = self.get_regionProps(masked_3D_labelmap)

        for prop in properties_3D_labelmap:
            labels.append(prop['label'])
        
        self.result['labels_neurons'] = labels
        self.make_new_folder(self.folder, 'labels_neurons')
        imsave(self.folder + 'labels_neurons/' + self.image_name, masked_3D_labelmap.astype(dtype=np.uint16))


    def get_results(self):
        self.get_total_labels()
        self.get_neuronal_counts()
        self.result['labels_progenitors'] = [label for label in self.result['labels_total'] if label not in self.result['labels_neurons']]
        self.result['total_count'] = len(self.result['labels_total'])
        self.result['neuron_count'] = len(self.result['labels_neurons'])
        self.result['progenitor_count'] = len(self.result['labels_progenitors'])
        self.result['percentage_neurons'] = (self.result['neuron_count'] / self.result['total_count']) * 100
        self.result['percentage_progenitors'] = (self.result['progenitor_count'] / self.result['total_count']) * 100
        return self.result

    
# counter = CellCounter(labelmap_2D=labelmap_2D, labelmap_3D=labelmap_3D, mask_tel=labelmask_tel, mask_cell=labelmask_neur)
# counter.get_results()

    

