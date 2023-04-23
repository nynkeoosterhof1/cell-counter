from cellpose import models
from cellpose import utils
from cellpose import plot
from skimage.io import imsave, imread
from skimage.util import img_as_uint
import os

# Seems to work ok for 24hpf_fish1

PATH_DATA = '/data/p257464/staging/20220120_staging/input/'
PATH_RESULTS_2D = '/data/p257464/staging/20220120_staging/labelmaps_2D/'
PATH_RESULTS_3D = '/data/p257464/staging/20220120_staging/labelmaps_3D/'

image_files = os.listdir(PATH_DATA) 

model = models.Cellpose(gpu=True, model_type='nuclei')
channels = [0,0]

for file in image_files:
  img = imread(PATH_DATA + file) 
  masks, flows, styles, diams = model.eval(img, diameter=30, flow_threshold=0.99, mask_threshold=-6, channels=channels, z_axis=0, do_3D=False, stitch_threshold=0.58)
  labelmap_3D = img_as_uint(masks)
  imsave(PATH_RESULTS_3D + file, labelmap_3D)
  masks, flows, styles, diams = model.eval(img, diameter=30, flow_threshold=0.99, mask_threshold=-6, channels=channels, z_axis=0, do_3D=False)
  labelmap_2D = img_as_uint(masks)
  imsave(PATH_RESULTS_2D + file, labelmap_2D)
  