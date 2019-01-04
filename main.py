from depth import Depth
from reference import Reference
from score import Score
from output import Output
import argparse
import sys


if name == "__main__":

    pdbs = None
    depth_files = None
    depth_path = None
    out = None

    parser = argparse.ArgumentParser(description='MoDS: Model Validation using Chemical Labelling and Residue Depth')
    parser.add_argument('-data', nargs=1,
                        help='specify experimental data: -data <input_data.txt>')
    parser.add_argument('-pdbs', nargs="+",
                        help='specify input pdbs: -mod_xl <model_data.pdb>')
    parser.add_argument('-depth_files', nargs="+",
                        help='specify input depth files: -depth_files <model-residue.depth>')
    parser.add_argument('-depth_path', nargs=1,
                        help='specify path to DEPTH installation (default to DEPTH)')
    parser.add_argument('-out', nargs=1,
                        help='specify output file location (will append .txt if not specified)')
    args = parser.parse_args()

    if args.data:
        referee = args.data[0]
    else:
        print("Please specify the experimental data file, use -h flag for help.")
        sys.exit()

    if args.pdbs:
        pdbs = args.pdbs

    if args.depth_files:
        depth_files = args.depth_files

    exp_list = Reference(referee).get_residues()

    models = {}

    if pdbs and not depth_files:
        for pdb in pdbs:
            depth = Depth(pdb_structure, None,depth_path)
            models[pdb.split('.')[0]] = Score(depth, exp_list).score_mono()
    elif depth_files:
        for depth_file in depth_files:
            depth = Depth(None, depth_file, depth_path)
            models[pdb.split('.')[0]] = Score(depth, exp_list).score_mono()
    else:
        print("Please specify pdbs or depth files, use -h flag for help.")
        sys.exit()
