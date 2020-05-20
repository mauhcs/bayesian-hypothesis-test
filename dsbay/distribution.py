import matplotlib
import numpy as np
import matplotlib.pyplot as plt


class DistributionMass:

    def __init__(self, x=None, y=None, distribution_dict=None):
        if distribution_dict is not None:
            assert isinstance(distribution_dict, dict)
            self.dist = distribution_dict
        if (x is not None) | (y is not None):
            assert isinstance(x, list)
            assert isinstance(y, list)
            assert len(x) == len(y)

            self.dist = {_x:_y for (_x,_y) in zip(x,y)}
        

    def get_HDI(self, credMass=0.95):
        probMassVec = list(self.dist.values())
        probMassArr = np.sort(np.array(probMassVec))[::-1]
        threshold_ix = np.where(probMassArr.cumsum() >= credMass)[0][0]

        probMassList = list(self.dist.items())
        probMassOrderedArr = np.array(sorted(probMassList, key = lambda x: x[1], reverse=True))
        return {k:v for (k,v) in probMassOrderedArr[threshold_ix+1:]}

    def plot(self):
        x = list(self.dist.keys())
        y = list(self.dist.values())
        ci_dist = self.get_HDI()
        CIX = list(ci_dist.keys())
        CIY = list(ci_dist.values())
        # suggestions: cool, 
        colors = [matplotlib.cm.get_cmap('cool')(2*i/len(x)) for i in range(len(x))]
        plt.figure(figsize=(13,4))
        plt.bar(x, y, color=colors)
        ax = plt.gca()
        ax.bar(CIX, CIY, alpha=0.1, hatch = '//', label="Critical Area")        
        ax.get_yaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        plt.legend()
        return ax
