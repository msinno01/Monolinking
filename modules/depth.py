import subprocess

class Depth:
    def __init__(self, pdb_structure=None, depth_file=None, depth_path=None):
        self.depth_file = self.read_depth(depth_file)

        if not pdb_structure and not depth_file:
            raise Exception("Please provide either PDB Structure or Depth File")
        elif pdb_structure and not depth_file:
            if depth_path:
                self.depth_file = self.run_depth(pdb_structure, depth_path)
            else:
                self.depth_file = self.run_depth(pdb_structure)

    def run_depth(self, pdb_structure, depth_path=None):
        print("Running Depth on {0}".format(pdb_structure))

        if not depth_path:
            cmd = ["DEPTH", "-i", pdb_structure, "-o", pdb_structure.split('.')[0]]
        else:
            cmd = [depth_path, "-i", pdb_structure, "-o", pdb_structure.split('.')[0]]

        ext_depth = subprocess.Popen(cmd)
        ext_depth.communicate()

        try:
            test_open = open("{0}-residue.depth".format(pdb_structure.split('.')[0]))
            test_open.close
        except:
            print "No depth file created - please ensure depth is installed: http://cospi.iiserpune.ac.in/depth/htdocs/download.html"
            exit(1)

        return self.read_depth("{0}-residue.depth".format(pdb_structure.split('.')[0]))

    def read_depth(self,depth_file):
        if not depth_file:
            return
        else:
            residues = {}
            print("Reading depth file {0}".format(depth_file))
            with open(depth_file,'r') as f:
                g = f.read().splitlines()
                for line in g[1:]:
                    id = int(line.split()[0].split(':')[1])
                    chain = line.split()[0].split(':')[0]
                    depth = float(line.split()[2])
                    residues[chain, id] = depth
                f.close()
            return residues

    def get_depth_at_res(self, chain, id):
         return self.depth_file[chain, int(id)]

    def get_depth_dict(self):
        return self.depth_file
