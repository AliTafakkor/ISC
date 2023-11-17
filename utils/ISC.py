import numpy as np


def calculate_ISC(data, subjects:range, method='pairwise-mean', n_g1=None):
    # Calculate ISC
    n_subjects = len(subjects)
    mask = np.tril(np.ones(n_subjects, dtype=bool), k=-1)

    # Initialization
    n_rois = data['L'].shape[0]
    if ((method == 'pairwise-mean') |
        (method == 'pairwise-mat') |
        (method == 'loo')):
        ISC = {'L':[], 'R':[]}
    elif method == 'pairwise-mixed':
        ISC = {'b_L':[], 'b_R':[], # contain between groups correlattions
               'w_g1_L':[], 'w_g1_R':[], # contain within group1 correlattions
               'w_g2_L':[], 'w_g2_R':[] # contain within group2 correlattions
               }
        mask_b = np.zeros((len(subjects),)*2, dtype=bool)
        mask_b[n_g1:, :n_g1] = 1
        mask_wg1 = np.zeros((len(subjects),)*2, dtype=bool)
        mask_wg1[:n_g1,:n_g1] = 1
        mask_wg1 = mask_wg1 & mask
        mask_wg2 = np.zeros((len(subjects),)*2, dtype=bool)
        mask_wg2[n_g1:,n_g1:] = 1
        mask_wg2 = mask_wg2 & mask
    elif ((method == 'Xloo') |
          (method == 'Xloo2')):
        ISC = {'CL':[], 'CR':[],
               'XL':[], 'XR':[]
               }
        
    for h in ['L','R']:
        for roi in range(1,n_rois):
            corr_mat = np.corrcoef(data[h][roi,subjects,:])
            if method == 'pairwise-mean':
                ISC[h].append(corr_mat[mask].mean())
            elif method == 'pairwise-mat':
                ISC[h].append(corr_mat)
            elif method == 'pairwise-mixed':
                ISC[f'b_{h}'].append(corr_mat[n_g1:, :n_g1]) # dimensions: n_g2 x n_g1
                ISC[f'w_g1_{h}'].append(corr_mat[mask_wg1])
                ISC[f'w_g2_{h}'].append(corr_mat[mask_wg2])
            elif method == 'loo':
                for s in subjects:
                    subjects_loo = [x for x in subjects if x != s]
                    subject_int = data[h][roi,s,:]
                    subjects_mean = np.mean(data[h][roi,subjects_loo,:], axis=0)
                    corr = np.corrcoef(subject_int, subjects_mean)
                    ISC[h].append(corr)
            elif method == 'Xloo':
                g2_mean = np.mean(data[h][roi,range(n_g1,n_subjects),:], axis=0)
                isc = []
                for s in range(n_g1):
                    subject_int = data[h][roi,s,:]
                    corr = np.corrcoef(subject_int, g2_mean)
                    isc.append(corr[0,1])
                ISC[f'X{h}'].append(isc)
                isc = []
                for s in range(n_g1,n_subjects):
                    subjects_loo = [x for x in range(n_g1,n_subjects) if x != s]
                    subject_int = data[h][roi,s,:]
                    subjects_mean = np.mean(data[h][roi,subjects_loo,:], axis=0)
                    corr = np.corrcoef(subject_int, subjects_mean)
                    isc.append(corr[0,1])
                ISC[f'C{h}'].append(isc)
            elif method == 'Xloo2':
                isc = []
                for s in range(n_g1): # iterate on subjects in group 1
                    temp = []
                    subject_g1 = data[h][roi,s,:]
                    for s2 in range(n_g1,n_subjects):
                        # leave one subject out from group 2
                        subjects_loo = [x for x in range(n_g1,n_subjects) if x != s2]
                        g2_subjects_mean = np.mean(data[h][roi,subjects_loo,:], axis=0)
                        
                        corr = np.corrcoef(subject_g1, g2_subjects_mean)
                        temp.append(corr[0,1])
                    isc.append(temp)
                ISC[f'X{h}'].append(isc)
                isc = []
                for s in range(n_g1,n_subjects):
                    subjects_loo = [x for x in range(n_g1,n_subjects) if x != s]
                    subject_int = data[h][roi,s,:]
                    subjects_mean = np.mean(data[h][roi,subjects_loo,:], axis=0)
                    corr = np.corrcoef(subject_int, subjects_mean)
                    isc.append(corr[0,1])
                ISC[f'C{h}'].append(isc)
                    

    return {key: np.array(value) for key, value in ISC.items()}
