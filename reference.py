class Reference:
    def __init__(self, in_file):
        self.residues = []
        with open(in_file,'r') as f:
            g = f.read().splitlines()
            for line in g:
                self.residues.append((line.split('|')[0], line.split('|')[1]))

    def get_residues(self):
        return self.residues()
