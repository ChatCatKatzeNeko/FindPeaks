'''
Author: Siyun WANG
'''
import numpy as np

class findPeaks():
    def __init__(self, signal, maxDepth, minWidth, percentile=50):
        '''
        Recursively finds all the peaks by finding their starting point and the width using 
        signal: array-like object, input signal whose local maximum to be found.
        maxDepth: positive integer, maximum depth of the binary search tree. The larger the more local maximum will be found, but may also include more noise.
        minWidth: positive integer, minimum width of the found "peak". This also constrains the depth of the binary search tree.
        percentile: integer between 0 and 100, optional, default to 50.
                    The threshold greater than which values are considered to be potential peaks and will be scanned by the binary searching process
        '''
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
        # get contiguous sub-sequences of values greater than the threshold defined by percentile
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
        # here expands the "binary search tree"
        for i in range(len(subStartInds)):
            if (subWidths[i] <= self.minWidth) | (depth+1 > self.maxDepth):
                self.rslt.append((subStartInds[i],subWidths[i]))
                continue
            self.scan_peaks_dicho(subStartInds[i], subWidths[i], depth+1)
