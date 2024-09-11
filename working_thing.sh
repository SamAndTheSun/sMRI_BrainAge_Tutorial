: "
Steps for analyzing mri data:

  Get metadata from dicom files
  Convert dicom files to nii and niigz
  Recon nii and niigz
  Convert brain.mgz file, as ouputted by freesurfer, to NPY format
  Format and apply neural network to NPY file 
  Generate 4d saliency map showing neural network weighting across subjects
  Compress this into 2d maps for further analysis
"

#set paths
INPUT_PATH = '/path_to_your_dicom_directory' #should be a folder of folders containing .dcm files
OUTPUT_PATH = '/path_to_your_output_directory' #should be an empty folder

#use python to get metadata from raw dicoms, and save this to "metadata.xlsx"
echo "from pyscripts import get_metadata; metadata, folder_order = get_metadata('$INPUT_PATH', '$OUTPUT_PATH')" | python3


#convert dicom files to nii or nii.gz format
dcm2niix '$INPUT_PATH' --OutDirMode=1 --OutDir='$OUTPUT_PATH' > log_file.txt

#select all of the files you want to run conversion on
RAW_FILES = $(find '$OUTPUT_PATH' -type f \(-name '*.nii' -o '*.nii.gz'\))

#specify and create the directory to output recons too
RECON_DIR = '/path_to_your_recon_directory'
mkdir -p "$RECON_DIR"

#run parallel processing of nii recons
parallel --jobs 4 'recon-all -i {} -sd '"$RECON_PATH"' -all' ::: $RAW_FILES

#identify all brain.mgz files, and convert these to a single NumPy array using NiBabel
#MIGHT NEED TO DOWNSAMPLE FIRST, BUT TRY WITHOUT FIRST
#PYTHON SCIPT HERE

#split the data, then train, validate, and test using a neural network to predict xyz
#PYTHON SCRIPT HERE

#generate a saliency map for the neural network, identifying which parts of the brain most strongly contributed to analysis
#PYTHON SCRIPT HERE

#compress the 4-dimensional saliency map into a 3-dimensional map by averaging across all subjcts
#PYTHON SCRIPT HERE

#visualize this three dimension map
#MATLAB SCRIPT HERE, SHOULD BE EASIER THAN COMPRESSING TO 2D
