class Reference:
        '''
        A class to handle the input file for experimental data.

        Data should be in a text file with the following format:

        1|A
        2|B
        ^ ^
        | |
        r c
        e h
        s a
        n i
        u n
        m
        b
        e
        r
        '''
    def __init__(self, in_file):
        self.residues = []
        with open(in_file,'r') as f:
            g = f.read().splitlines()
            for line in g:
                self.residues.append((line.split('|')[1], int(line.split('|')[0])))

    def get_residues(self):
        return self.residues
