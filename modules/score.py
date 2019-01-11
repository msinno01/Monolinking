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

    def weighted_step_score(self):
        score = 0
        for chain, id in self.exp_list:
            res_score = self.depth_object.get_depth_at_res(chain, id)
            if res_score < 2:
                score -= res_score*10
            elif res_score >= 2 and < 4:
                score -= res_score*8
            elif res_score >= 4 and < 6:
                score -= res_score*6
            elif res_score >= 6 and < 8:
                score -= res_score*4
            elif res_score >= 8 and < 10:
                score -= res_score*2
            elif res_score >= 10:
                score -= res_score

        return score

    def linear_function_score(self):
        score = 0
        z = [  0.02232143  -1.15178571  10.10714286]
        p = np.poly1d(z)
        for chain, id in self.exp_list:
            res_score = self.depth_object.get_depth_at_res(chain, id)
            if res_score < 10:
                score -= res_score*p(res_score)
            else:
                score -= res_score
        return score

    def exp_fit(self, res_score):
        return 9 * np.exp(-0.5*res_score)+1

    def exponential_function_score(self):
        score = 0
        for chain, id in self.exp_list:
            res_score = self.depth_object.get_depth_at_res(chain, id)
            score -= self.exp_fit(res_score)
        return score
