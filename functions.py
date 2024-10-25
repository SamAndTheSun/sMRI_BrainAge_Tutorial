import os
import glob
import dcmread

import numpy as np
import pandas as pd
import nibabel as nib

def get_metadata(input_dir, folder_pattern = '/*/.dcm'):
    """
    Iterate through all of the available dicom-containing folders. Select a single
    dicom file from each of this (since they presumably have the same metadata for the same
    scan), and extract the metadata. Then, add this to a dataframe

    param input_dir: the folder containing the scan folders
    param folder_pattern: the folder tree structure
        e.g. input_dir/subject/scans.dcm = /*/*.dcm
    """

    # get all folders containing dcm files
    folders = glob.glob(input_dir + folder_pattern)

    metadata = []

    for folder in folders:
        dcm_files = glob.glob(folder + '*.dcm') # for some datasets this may not be sufficient
        ds = dcmread(dcm_files[0]) # metadata should be identical for all dicoms in the same subject/timepoint folder
        
        # get all of the metadata from the dictionary
        file_metadata = {}
        for e in ds.iterall():
            tag_name = e.name
            file_metadata[tag_name] = e.value

        # add the metadata for the file
        metadata.append(file_metadata)

    metadata_df = pd.DataFrame(metadata)
    return metadata_df



