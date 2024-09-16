import os
import glob
import dcmread

import numpy as np
import pandas as pd
import nibabel as nib

def get_metadata(input_dir, out_dir, folder_pattern = '/*/.dcm'):

    #get all folders containing dcm files
    folders = glob.glob(input_dir + folder_pattern)

    metadata = []

    for folder in folders:
        dcm_files = glob.glob(folder + '*.dcm')
        ds = dcmread(dcm_files[0]) #metadata should be identical for all dicoms in the same subject/timepoint folder
        
        #get all of the metadata from the dictionary
        file_metadata = {}
        for e in ds.iterall():
            tag_name = e.name
            file_metadata[tag_name] = e.value

        #add the metadata for the file
        metadata.append(file_metadata)

    metadata_df = pd.DataFrame(metadata)
    metadata_df['File Path'] = folders
    metadata.to_excel(out_dir + 'metadata.xlsx')
    
    return

def mgz_to_np(metadata_dir, out_dir):
    '''
    converts several mgz files into a single NumPy array, fit for NN analysis
    depending on the NN, you may need to downsample the mgz files accordingly
    '''

    metadata.from_excel(out_dir + 'metadata.xlsx')
    files_paths = list(metadata['File Path'])

    array = []

    for path in file_paths:
        img = nib.load(path)
        data = img.get_fdata() #convert data to numPy array

        #from scipy.ndimage import zom; zoom(input, (0.5, 0.5, 0.5)
        
        array.append(data)

    np_array = np.stack(array, axis=0)
    np.save(out_dir + 'metadata.xlsx', np_array)
    
    return
    
def build_CNN(x_dim=128, y_dim=128, z_dim=128, n_channels=1):

    raw_input = tf.keras.Input((x_dim, y_dim, z_dim, n_channels))
    x = tf.keras.layers.Conv3D(filters=, kernel_size_=, activation='relu')(raw_input)

    etc.

    outputs = tf.keras.layers.Dense(units=1, activation='relu')(x)
    
    model = keras.Model(inputs, outputs) #create the model class
    return model

def process_saliency_mapy():
    #first, you want to get the atlas data for the individual subject. This is available in the a2009+aseg.mgz file
    #it is a "brain segmentation map", so in order to interpret the saliency map you want to start with this

    #next, try using "zoom" or something similar so it in the same dimensions as the saliency map

    #maybe you could also just use the fact that you know its subjects, x, y, z, with x y and z being 256. You average across subject axis. Then, you use 

    
    

