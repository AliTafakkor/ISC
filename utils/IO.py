import h5py
import glob
import os
import pandas as pd
import numpy as np

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


def load_runs_HDF(runs_df, n_vols):
    """Load data stored in the HDF files given the runs dataframe."""
    # Loading only the last run
    with h5py.File(runs_df['full_path'].iloc[-1], 'r') as f:
            # Load the parcellated data
            data = f['parcellated_data'][:]
            data = data[:,:n_vols] # Ignoring excessive volumes
    return data


def load_subjects(df, subjects, n_vols):
    data = {'L':[], 'R':[]}
    for i, subj in enumerate(subjects):
        # Filter subject
        df_s = df[df['subject'] == subj]
        # Load Left and Right hemispheres
        for h in ['L', 'R']:
            data[h].append(load_runs_HDF(df_s[df_s['hemi'] == h], n_vols))

    # for Lett and Right hemispheres
    for h in ['L', 'R']:
        # Stacking subjects data (Subject, ROI, Time)
        data[h] = np.stack(data[h])
        # Organizing data in (ROI, Subject, Time) shape for more efficient slicing when calculating ISCs
        data[h] = np.transpose(data[h], axes=(1, 0, 2))
    
    return data