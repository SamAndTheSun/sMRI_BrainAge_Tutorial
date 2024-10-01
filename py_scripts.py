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
        #you want to do this because 256 is easier processing wise for a NN
        
        array.append(data)

    np_array = np.stack(array, axis=0)

    #maybe normalize data here?
    
    np.save(out_dir + 'metadata.xlsx', np_array)
    
    return
    
def build_CNN(x_dim=128, y_dim=128, z_dim=128, n_channels=1):
 
    inputs = tf.keras.Input((x_dim, y_dim, z_dim, n_channels))
 
    x = tf.keras.layers.Conv3D(filters=16, kernel_size=4, activation="relu")(inputs)
    x = tf.keras.layers.MaxPool3D(pool_size=(2, 2, 2))(x)
    x = tf.keras.layers.BatchNormalization()(x)
 
    x = tf.keras.layers.Conv3D(filters=32, kernel_size=6, activation="relu")(x)
    x = tf.keras.layers.MaxPool3D(pool_size=(2, 2, 2))(x)
    x = tf.keras.layers.BatchNormalization()(x)

    x = tf.keras.layers.GlobalAveragePooling3D()(x)
    x = tf.keras.layers.Dense(units=128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.5)(x)
 
    outputs = tf.keras.layers.Dense(units=1, activation="relu")(x)
 
    model = keras.Model(inputs, outputs)
    return model

    #this wouldn't be useful for vizualition, but if I combine that with 3d rendering it should be easier than trying to figre out the matlab code fully 
    

