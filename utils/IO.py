import h5py
import glob
import os
import pandas as pd

def get_dimensions(filepath):
    """Extract dimensions of data from h5 data."""
    # Open the HDF5 file
    with h5py.File(filepath, 'r') as f:
        # Load the parcellated data
        data = f['parcellated_data'][:]
        # Return data dimensions
        n_rois, n_vol = data.shape
    return n_rois, n_vol


def get_info(filepath):
    """Extract subject, hemi, task, run, fwhm, confounds,
      rois, and number of volumes from a given file."""
    # Get file name
    basename = os.path.basename(filepath)
    # Split file name by '_'
    parts = basename.split('_')
    # Info dictionary
    info = {}
    # Parse file name
    for part in parts:
        info['full_path'] = filepath

        if part.startswith('sub-'):
            info['subject'] = part.split('sub-')[1]
        elif part.startswith('hemi-'):
            info['hemi'] = part.split('hemi-')[1]
        elif part.startswith('task-'):
            info['task'] = part.split('task-')[1]
        elif part.startswith('run-'):
            info['run'] = part.split('run-')[1]
        elif part.startswith('fwhm-'):
            info['fwhm'] = part.split('fwhm-')[1]
        elif part.startswith('confounds-'):
            info['confounds'] = part.split('confounds-')[1].split('_')[0]  # Assuming confounds is the last part before the file extension

    # Get dimensions for stored data    
    info['n_roi'], info['n_vol'] = get_dimensions(filepath)
    
    return info


def build_dataframe(directory):
    """Build a dataframe from files in the directory and its subdirectories."""
    # Pattern for search
    subject, hemi, task, run, fwhm, confounds = ('*', '*', '*', '*', 0, 5)   
    pattern = os.path.join(directory, '**', f"sub-{subject}_hemi-{hemi}_task-{task}_run-{run}_space-fsLR_den-32k_desc-denoised_fwhm-{fwhm}_confounds-{confounds}_atlas-glasser.h5")
    # Get all files matching the pattern
    files = glob.glob(pattern, recursive=True)
    # Building the dataframe
    df = pd.DataFrame([get_info(file) for file in files])
    
    return df
