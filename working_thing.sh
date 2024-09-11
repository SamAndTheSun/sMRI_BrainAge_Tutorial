: '
Steps for analyzing mri data:

  Get metadata from dicom files
  Convert dicom files to nii and niigz
  Recon nii and niigz
  Convert brain.mgz file, as ouputted by freesurfer, to NPY format
  Format and apply neural network to NPY file 
  Generate 4d saliency map showing neural network weighting across subjects
  Compress this into 2d maps for further analysis
'

#set paths
INPUT_PATH = '/path_to_your_dicom_directory'
OUTPUT_PATH = '/path_to_your_output_directory'

#get metadata from dicom files

#convert dicom files to nii or nii.gz format
dcm2niix '$INPUT_PATH' --OutDirMode=1 --OutDir='$OUTPUT_PATH' > log_file.txt

#select all of the files you want to run conversion on
RAW_FILES = $(find '$OUTPUT_PATH' -type f \(-name '*.nii' -o '*.nii.gz'\))

#specify and create the directory to output recons too
RECON_DIR = '/path_to_your_recon_directory'
mkdir -p "$RECON_DIR"

#run parallel processing of nii recons
parallel --jobs 4 'recon-all -i {} -sd '"$RECON_PATH"' -all' ::: $RAW_FILES

#identify all brain.mgz files, and convert these to a single NumPy array
