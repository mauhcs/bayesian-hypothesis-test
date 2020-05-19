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
        thetaValues = list(self.dist.keys())
        probMassArr = np.sort(np.array(probMassVec))[::-1]
        arr = np.where(probMassArr.cumsum()>= credMass)
        heightIX = arr[0][0]
        if heightIX == 0: # If one discrete value is enough for the credMass threashold
            r = thetaValues[probMassVec.index(probMassArr[0])]
            return r, r
        IXS = [probMassVec.index(probMassArr[i]) for i in range(heightIX+1)]
        _left  = min(thetaValues[min(IXS)], thetaValues[max(IXS)])
        _right = max(thetaValues[min(IXS)], thetaValues[max(IXS)])
        return _left, _right+1

    def plot(self):
        x = list(self.dist.keys())
        y = list(self.dist.values())
        _left, _right = self.get_HDI()
        CIX = x[:x.index(_left)+1], x[x.index(_right):]
        CIY = y[:x.index(_left)+1], y[x.index(_right):]
        # suggestions: cool, 
        colors = [matplotlib.cm.get_cmap('cool')(2*i/len(x)) for i in range(len(x))]
        plt.bar(x, y, color=colors)
        ax = plt.gca()
        ax.bar(CIX[0], CIY[0], alpha=0.1, hatch = 'x')
        ax.bar(CIX[1], CIY[1], alpha=0.1, hatch = 'x', label="Critical Area")
        plt.legend()
        plt.show()
        return ax
