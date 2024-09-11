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

def mgz_to_np(file_paths, out_dir):
    '''
    converts several mgz files into a single NumPy array, fit for NN analysis
    depending on the NN, you may need to downsample the mgz files accordingly
    '''

    array = []

    for path in file_paths:
        img = nib.load(path)
        data = img.get_fdata() #convert data to numPy array
        array.append(data)

    np_array = np.stack(array, axis=0)
    np.save(out_dir + 'metadata.xlsx', np_array)
    
    return
    


