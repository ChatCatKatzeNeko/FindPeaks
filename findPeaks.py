import numpy as np

class findPeaks():
    def __init__(self, signal, maxDepth, minWidth, percentile=50):
        self.signal = signal
        self.maxDepth = maxDepth
        self.minWidth = minWidth
        self.percentile = percentile
        self.rslt = []
        
    def scan_peaks_dicho(self, startInd, width, depth):
        val = np.percentile(self.signal[startInd:startInd+width],self.percentile)
        isPeak = (self.signal[startInd:startInd+width]>=val)

        subStartInds = []
        subWidths = []
        counter = 0
        for j in range(len(isPeak)):
            if isPeak[j]:
                if counter == 0:
                    subStartInds.append(j)
                counter +=1
            else:
                if counter > 0:
                    subWidths.append(counter)
                counter = 0   
        if len(subWidths) == len(subStartInds)-1:
            subWidths.append(counter)

        subStartInds,subWidths = np.array(subStartInds)+startInd,np.array(subWidths)

        for i in range(len(subStartInds)):
            if (subWidths[i] <= self.minWidth) | (depth+1 > self.maxDepth):
                self.rslt.append((subStartInds[i],subWidths[i]))
                continue
            self.scan_peaks_dicho(subStartInds[i], subWidths[i], depth+1)
