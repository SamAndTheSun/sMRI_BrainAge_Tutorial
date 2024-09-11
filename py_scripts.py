import glob
import dcmread

def get_metadata(raw_dir, folder_pattern = '/*/.dcm'):

    #get all folders containing dcm files
    folders = glob.glob(raw_dir + folder_pattern)

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

    return metadata, folders #useful in determining sort order for later analysis
    


