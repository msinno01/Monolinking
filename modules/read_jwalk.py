from depth import Depth
import sys
import subprocess

class ReadJwalk:
    def __init__(self, jwalk_file=None, pdb_structure=None, jwalk_path=None):
        if jwalk_file:
            self.read_jwalk(jwalk_file)
        elif pdb_structure and not jwalk_file:
            self.run_jwalk(pdb_structure, jwalk_path)
        else:
            print("Please provide Jwalk input or pdb file.")
            sys.exit()

        self.intra = {}
        self.inter = {}

    def read_jwalk(self, jwalk_file):
        with open(jwalk_file, 'r') as f:
            g = f.read().splilines()
            for line in g[1:]:
                aa1 = int(line.split()[2].split('-')[1])
                c1 = line.split()[2].split('-')[2]
                aa2 = int(line.split()[3].split('-')[1])
                c2 = line.split()[3].split('-')[2]
                SASD = float(line.split()[4])

                if c1 == c2:
                    if int(aa1) < int(aa2):
                        low = aa1
                        low_chain = c1
                        high = aa2
                        high_chain = c2
                    else:
                        low = aa2
                        low_chain = c2
                        high = aa1
                        high_chain = c1
                    self.intra[low, low_chain, high, high_chain] = SASD
                else:
                    if int(aa1) < int(aa2):
                        low = aa1
                        low_chain = c1
                        hi = aa2
                        hi_chain = c2
                    else:
                        low = aa2
                        low_chain = c2
                        hi = aa1
                        hi_chain = c1
                    self.inter[low, low_chain, high, high_chain] = SASD

    def run_jwalk(self, pdb_structure, jwalk_path="jwalk"):
        cmd = [jwalk_path, "-i", pdb_structure,"-surface_depth"]
        ext_jwalk = subprocess.Popen(cmd)
        ext_jwalk.communicate()

        self.read_jwalk("Jwalk_results/{0}_crosslink_list.txt".format(pdb_structure.split(".pdb")[0]))

    def get_intra_crosslinks(self):
        return self.intra_crosslinks

    def get_inter_crosslinks(self):
        return self.inter_crosslinks

    def get_sasd_at_intra(self, low, low_chain, high, high_chain):
        if (low, low_chain, high, high_chain) in self.intra.keys():
            return self.intra[low, low_chain, high, high_chain]
        else:
            return False

    def get_sasd_at_inter(self, low, low_chain, high, high_chain):
        if (low, low_chain, high, high_chain) in self.inter.keys():
            return self.inter[low, low_chain, high, high_chain]
        else:
            return False
