#Steps:

#

#set pathss
INPUT_PATH = '/path_to_your_dicom_directory'
OUTPUT_PATH = '/path_to_your_output_directory'

#convert dicom files to nii or nii.gz format
dcm2niix '$INPUT_PATH' --OutDirMode=1 --OutDir='$OUTPUT_PATH'> log_file.txt

#select all of the files you want to run conversion on
RAW_FILES = $(find '$OUTPUT_PATH' -type f \(-name '*.nii' -o '*.nii.gz'\))

#specify and create the directory to output recons too
RECON_PATH = '/path_to_your_recon_directory'

#run parallel processing of nii recons
parallel --jobs 4 'recon-all -i {} -sd $RECON_PATH -all ::: $RAW_FILES




#next, add a subjects directory for freesurfer
