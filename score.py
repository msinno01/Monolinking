class Score:
    def __init__(self,depth_object, exp_list):
        self.exp_dict = exp_dict
        self.depth_object = depth_object

    def score_mono(self):
        score = 0
        for chain, id in self.exp_list:
            score -= self.depth_object.get_depth_at_res(chain, id)
        return score
