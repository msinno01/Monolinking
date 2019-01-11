from modules.depth import Depth
from modules.reference import Reference
from modules.score import Score_monolinks
from modules.output import Output
import argparse
import sys

def run_mono(pdbs, depth_files, mono_list, depth_path=None):
    models = {}
    if pdbs and not depth_files:
        for pdb in pdbs:
            depth = Depth(pdb, None, depth_path)
            models[pdb.split('.pdb')[0]] = Score(depth, mono_list).score_mono()
        return models
    elif depth_files:
        for depth_file in depth_files:
            depth = Depth(None, depth_file, depth_path)
            models[depth_file.split('-residue.depth')[0]] = Score(depth, mono_list).score_mono()
        return models
    else:
        print("Please specify pdbs or depth files, use -h flag for help.")
        sys.exit()

def run_crosslink(pdbs, jwalk_files, intra_list=None, inter_list=None, jwalk_path=jwalk_path):
    if pdbs and not jwalk_files:
        for pdb in pdbs:
            jwalk = ReadJwalk(pdb_structure=pdb, jwalk_path)

if __name__ == "__main__":

    pdbs = None
    depth_files = None
    depth_path = None
    out = None
    jwalk_path = None

    parser = argparse.ArgumentParser(description='MoDS: Model Validation using Chemical Labelling and Residue Depth')
    parser.add_argument('-data', nargs=1,
                        help='specify experimental data: -data <input_data.txt>')
    parser.add_argument('-pdbs', nargs="+",
                        help='specify input pdbs: -mod_xl <model_data.pdb>')
    parser.add_argument('-depth_files', nargs="+",
                        help='specify input depth files: -depth_files <model-residue.depth>')
    parser.add_argument('-depth_path', nargs=1,
                        help='specify path to DEPTH installation (default to DEPTH)')
    parser.add_argument('-jwalk_files', nargs="+",
                        help='specify input jwalk files: -jwalk_files <model-residue.depth>')
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

    if args.out:
        out = args.out[0]

    ref = Reference(referee)
    mono_list = ref.get_monolinks()
    intra_list = ref.get_intra_crosslinks()
    inter_list = ref.get_inter_crosslinks()

    if mono_list:
        monolinks = run_mono(pdbs, depth_files, mono_list)

    if intra_list and not inter_list:
        intra = run_crosslink(pdbs, jwalk_files, intra_list=intra_list)


    Output(monolinks, out)
