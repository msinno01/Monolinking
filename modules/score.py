class Score:
    '''
    A class to handle scoring of residues from experimental data based on their depth in the structure. 
    '''
    def __init__(self,depth_object, exp_list):
        self.exp_list = exp_list
        self.depth_object = depth_object

    def score_mono(self):
        score = 0
        for chain, id in self.exp_list:
            score -= self.depth_object.get_depth_at_res(chain, id)
        return score
