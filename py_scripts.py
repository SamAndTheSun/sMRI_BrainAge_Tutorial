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

    raw_input = tf.keras.Input((x_dim, y_dim, z_dim, n_channels))
    x = tf.keras.layers.Conv3D(filters=, kernel_size_=, activation='relu')(raw_input)

    etc.

    outputs = tf.keras.layers.Dense(units=1, activation='relu')(x)
    
    model = keras.Model(inputs, outputs) #create the model class
    return model

def process_saliency_mapy():

import nibabel as nib
import matplotlib.pyplot as plt

    # Load the FreeSurfer parcellation file
    aparc_img = nib.load('aparc.a2009s+aseg.mgz')
    aparc_data = aparc_img.get_fdata()

    # Define the label for the region of interest (e.g., hippocampus)
    region_label = 17  # Example label for the left hippocampus
    
    # Create a mask for the region of interest
    region_mask = (aparc_data == region_label)

    # Load the saliency map
    saliency_img = nib.load('saliency_map.mgz')
    saliency_data = saliency_img.get_fdata()
    
    # Apply the mask to the saliency map
    region_saliency = saliency_data[region_mask]
    
    # Compute statistics for the region (optional)
    mean_saliency = region_saliency.mean()
    print(f'Mean Saliency for Region {region_label}: {mean_saliency}')

    # Optionally, display a 2D slice of the saliency data
    slice_index = saliency_data.shape[2] // 2
    plt.imshow(saliency_data[:, :, slice_index], cmap='jet')
    plt.colorbar()
    plt.title(f'Saliency Map Slice for Region {region_label}')
    plt.show()

    
    #first, you want to get the atlas data for the individual subject. This is available in the a2009+aseg.mgz file
    #it is a "brain segmentation map", so in order to interpret the saliency map you want to start with this
    #then from that you can get information about overlap

    #maybe, dont zoom, train the nn, use native.mgz for visualization?

    #this wouldn't be useful for vizualition, but if I combine that with 3d rendering it should be easier than trying to figre out the matlab code fully 
    

