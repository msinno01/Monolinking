import scipy.stats as sts
import numpy as np

class Score_monolinks:
    '''
    A class to handle scoring of monolinks from experimental data based on their depth in the structure.
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
        
class Score_crosslinks:
    def __init__(self, jwalk_object, intra_crosslinks, inter_crosslinks):
        self.jwalk_object = jwalk_object
        self.intra_crosslinks = intra_crosslinks
        self.inter_crosslinks = inter_crosslinks

        self.P_inter = 0
        self.P_intra = 0
        self.N_inter = 0
        self.N_intra = 0
        self.M_inter = 0
        self.M_intra = 0

    def score_intra(self):
        N = sts.norm(18.62089,5.995381)

        for xl1,c1,xl2,c2 in self.intra_crosslinks:
            SASD = jwalk_object.get_sasd_at_intra(xl1, c1, xl2, c2)
            if not SASD:
                self.M_intra += -0.1
            elif SASD <= 33:
                self.P_intra += N.pdf(SASD)
            else:
                self.N_intra += -0.1

    def score_inter(self):
        N = sts.norm(21.91883,4.871774)

        for xl1,c1,xl2,c2 in self.inter_crosslinks:
            SASD = jwalk_object.get_sasd_at_inter(xl1, c1, xl2, c2)
            if not SASD:
                self.M_inter += -0.1
            elif SASD <= 36:
                self.P_inter += N.pdf(SASD)
            else:
                self.N_inter += -0.1

    def generate_totals(self):
        self.inter_NPM = self.N_inter+self.P_inter+self.M_inter
        self.cMNXL = self.inter_NPM + self.M_intra*0.3
        self.MNXL = self.N_intra + self.M_intra + self.P_intra

    def get_MNXL(self):
        self.score_intra()
        self.generate_totals()
        return self.MNXL

    def get_cMNXL(self):
        self.score_inter()
        self.score_intra()
        self.generate_totals()
        return self.cMNXL
