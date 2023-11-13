import nibabel as nib
import numpy as np
import os

def roi2gii(roi_data, fpath, fname):
    """Create GIFTI Image from ROI values and save it in the results."""
    # Iterate on Left and Right hemispheres
    for hemi in ['L', 'R']:
        # Load atlas file for the hemisphere
        label_gii = nib.load(os.path.join('resources','surface_atlases',f'Glasser_2016.32k.{hemi}.label.gii'))
        label_data = label_gii.darrays[0].data
        # Copy ROI value to vertices 
        n_vertices = len(label_data)
        surface_values = np.zeros(n_vertices, dtype='float32')
        for roi_label, value in enumerate(roi_data[hemi]):
            vertices = (label_data == roi_label+1)
            surface_values[vertices] = value
        
        # Create a GIFTI data array for the map
        gii_darray = nib.gifti.GiftiDataArray(data=surface_values, intent=nib.nifti1.intent_codes['NIFTI_INTENT_SHAPE'])
        # Create a GIFTI image for the map
        gii_image = nib.gifti.GiftiImage(darrays=[gii_darray])
        # Save GIFTI image
        nib.save(gii_image, os.path.join(fpath,f'{fname}_{hemi}.shape.gii'))

    return surface_values
    