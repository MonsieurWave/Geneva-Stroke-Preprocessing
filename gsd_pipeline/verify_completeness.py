import os
import numpy as np
import pandas as pd


data_dir = '/Users/julian/temp/VPCT_extraction_test/extracted'

def verify_completeness_nifti(data_dir):
    subject_folders = [o for o in os.listdir(data_dir)
                    if os.path.isdir(os.path.join(data_dir,o))]
    print(len(subject_folders), 'subjects found.')
    state_columns = ['subject', 'hasT2', 'hasMTT', 'hasTmax', 'hasCBF', 'hasCBV', 'hasSPC', 'hasVOI', 'hasTRACE',
                     'hasADC', 'hasAngio', 'hasPCT']
    imaging_completeness_df = pd.DataFrame(columns=state_columns)
    all_complete = 1

    for folder in subject_folders:
        folder_dir = os.path.join(data_dir, folder)
        modalities = [o for o in os.listdir(folder_dir)
                        if os.path.isdir(os.path.join(folder_dir,o))]

        hasT2 = 0
        hasMTT = 0
        hasTmax = 0
        hasCBF = 0
        hasCBV = 0
        hasSPC = 0
        hasVOI = 0
        hasTRACE = 0
        hasADC = 0
        hasAngio = 0
        hasPCT = 0

        for modality in modalities:
            modality_dir = os.path.join(folder_dir, modality)
            studies = [f for f in os.listdir(modality_dir) if f.endswith(".nii")]
            for study in studies:
                if 't2_tse_tra' in study: hasT2 = 1
                if 'MTT' in study: hasMTT = 1
                if 'Tmax' in study: hasTmax = 1
                if 'CBF' in study: hasCBF = 1
                if 'CBV' in study: hasCBV = 1
                if 'SPC_301mm_Std' in study: hasSPC = 1
                if 'TRACE' in study: hasTRACE = 1
                if 'ADC' in study: hasADC = 1
                if 'Angio' in study: hasAngio = 1
                if 'VPCT' in study: hasPCT = 1

        # lesion files should be in subject dir
        nii_files = [f for f in os.listdir(folder_dir) if f.endswith(".nii")]
        for file in nii_files:
            if 'VOI' in file: hasVOI = 1

        conditions = [hasT2, hasMTT, hasTmax, hasCBF, hasCBV, hasSPC, hasVOI, hasTRACE, hasADC, hasAngio, hasPCT]
        condition_names = ['hasT2', 'hasMTT', 'hasTmax', 'hasCBF', 'hasCBV', 'hasSPC', 'hasVOI', 'hasTRACE', 'hasADC',
                           'hasAngio', 'hasPCT']

        if np.all(conditions):
            print(folder, 'is complete.')
        else:
            missing_files = np.array(condition_names)[np.where(np.array(conditions) < 1)[0]]
            print(folder, 'is missing', missing_files)
            imaging_completeness_df = imaging_completeness_df.append(
                pd.DataFrame([[folder, hasT2, hasMTT, hasTmax, hasCBF, hasCBV, hasSPC, hasVOI, hasTRACE, hasADC,
                               hasAngio, hasPCT]],
                columns = state_columns),
                ignore_index=True)
            all_complete = 0

    imaging_completeness_df.to_excel(os.path.join(data_dir, 'imaging_completeness.xlsx'))

    return bool(all_complete)

def verify_completeness_dcm(data_dir):
    subject_folders = [o for o in os.listdir(data_dir)
                       if os.path.isdir(os.path.join(data_dir, o))]
    print(len(subject_folders), 'subjects found.')
    state_columns = ['subject', 'hasT2', 'hasMTT', 'hasTmax', 'hasCBF', 'hasCBV', 'hasSPC', 'hasVOI', 'hasTRACE',
                     'hasADC', 'hasAngio', 'hasVPCT']
    imaging_completeness_df = pd.DataFrame(columns=state_columns)
    all_complete = 1

    for folder in subject_folders:
        folder_dir = os.path.join(data_dir, folder)
        modalities = [o for o in os.listdir(folder_dir)
                      if os.path.isdir(os.path.join(folder_dir, o))]

        hasT2 = 0
        hasMTT = 0
        hasTmax = 0
        hasCBF = 0
        hasCBV = 0
        hasSPC = 0
        hasVOI = 0
        hasTRACE = 0
        hasADC = 0
        hasAngio = 0
        hasPCT = 0

        for modality in modalities:
            modality_dir = os.path.join(folder_dir, modality)
            studies = [f for f in os.listdir(modality_dir) if os.path.isdir(os.path.join(modality_dir, f))]
            for study in studies:
                if 't2_tse_tra' in study: hasT2 = 1
                if 'MTT' in study: hasMTT = 1
                if 'Tmax' in study: hasTmax = 1
                if 'CBF' in study: hasCBF = 1
                if 'CBV' in study: hasCBV = 1
                if 'SPC_301mm_Std' in study: hasSPC = 1
                if 'TRACE' in study: hasTRACE = 1
                if 'ADC' in study: hasADC = 1
                if 'Angio' in study: hasAngio = 1
                if 'VPCT' in study: hasPCT = 1

        # lesion files should be in subject dir
        nii_files = [f for f in os.listdir(folder_dir) if f.endswith(".nii")]
        for file in nii_files:
            if 'VOI' in file: hasVOI = 1

        conditions = [hasT2, hasMTT, hasTmax, hasCBF, hasCBV, hasSPC, hasVOI, hasTRACE, hasADC, hasAngio, hasPCT]
        condition_names = ['hasT2', 'hasMTT', 'hasTmax', 'hasCBF', 'hasCBV', 'hasSPC', 'hasVOI', 'hasTRACE', 'hasADC',
                           'hasAngio', 'hasPCT']

        if np.all(conditions):
            print(folder, 'is complete.')
        else:
            missing_files = np.array(condition_names)[np.where(np.array(conditions) < 1)[0]]
            print(folder, 'is missing', missing_files)
            imaging_completeness_df = imaging_completeness_df.append(
                pd.DataFrame([[folder, hasT2, hasMTT, hasTmax, hasCBF, hasCBV, hasSPC, hasVOI, hasTRACE, hasADC,
                               hasAngio, hasPCT]],
                             columns=state_columns),
                ignore_index=True)
            all_complete = 0

    imaging_completeness_df.to_excel(os.path.join(data_dir, 'imaging_completeness.xlsx'))

    return bool(all_complete)

if __name__ == "__main__":
    verify_completeness_dcm(data_dir)
