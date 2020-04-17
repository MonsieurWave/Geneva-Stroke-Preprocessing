import os, shutil, argparse
import nipype.interfaces.spm as spm
from nipype.interfaces.fsl import Split, Merge

def coregistration_4D(source_file, ref, out_file=None):
    '''
    Coregistration with spm + fsl for 4D files.
    Why? Nor SPM, nor fsl are able to do this by default
    :param source_file: path to input 4D file
    :param ref: reference file to co-register the source-file to
    :return: path to coregistered file
    '''
    main_dir, source_file_name = os.path.split(source_file)
    if out_file is None:
        out_file = os.path.join(main_dir, 'r' + source_file_name)

    split_folder = os.path.join(main_dir, '4D_split')
    os.mkdir(split_folder)
    split = Split(in_file=source_file, dimension='t')
    split.inputs.in_file = source_file
    split.inputs.dimension = 't'
    split.inputs.out_base_name = os.path.join(split_folder, '4D_vol_')
    split.inputs.output_type = 'NIFTI'
    split = split.run()

    split_files = split.outputs.out_files
    index_file = split_files.pop(0)

    coreg = spm.Coregister()
    coreg.inputs.target = ref
    coreg.inputs.mfile = False
    coreg.inputs.source = index_file
    coreg.inputs.apply_to_files = split_files
    coreg = coreg.run()

    merger = Merge()
    merger.inputs.in_files = coreg.outputs.coregistered_files
    merger.inputs.dimension = 't'
    merger.inputs.output_type = 'NIFTI_GZ'
    merger.inputs.merged_file = out_file
    merger = merger.run()

    shutil.rmtree(split_folder)

    return merger.outputs.merged_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Coregister 4D file to reference file')
    parser.add_argument('input_file')
    parser.add_argument('-ref', action="store", dest='ref', help='Reference file to coregister to')
    args = parser.parse_args()
    coregistration_4D(args.input_file, args.ref)