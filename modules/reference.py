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
        self.monolinks = []
        self.intra = []
        self.inter = []
        crosslinks = []

        with open(in_file,'r') as f:
            g = f.read().splitlines()
            for line in g:
                if len(line.split('|')) < 4:
                    self.monolinks.append((line.split('|')[1], int(line.split('|')[0])))
                else:
                    crosslinks.append((line.split('|')[1], int(line.split('|')[0], line.split('|')[2], line.split('|')[3])))
            f.close()

        if crosslinks:
            self.handle_crosslinks(crosslinks)

    def handle_crosslinks(self, crosslinks):
        chains = []
        #handling crosslinks
        for c1, aa1, c2, aa2 in crosslinks:
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
                self.intra.append([low, low_chain, high, high_chain])
            else:
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

                self.inter.append([low,low_chain,high,high_chain])

            if c1 not in chains:
                chains.append(c1)
            if c2 not in chains:
                chains.append(c2)

        if len(chains) > 1:
            self.complex = 1
        else:
            self.complex = 0

    def get_monolinks(self):
        return self.monolinks

    def get_intra_crosslinks(self):
        return self.intra_crosslinks

    def get_inter_crosslinks(self):
        return self.inter_crosslinks

    def get_crosslinks(self):
        if self.complex:
            return self.intra_crosslinks + self.inter_crosslinks
        else:
            return self.intra_crosslinks
