from scipy.fft import idctn
import numpy as np

def idct_on_splits(Y_splits, Cb_splits, Cr_splits):
    num, _, _ = Y_splits.shape
    
    for i in range(num):
        Y_splits[i] = idctn(Y_splits[i], type=2)
        Cb_splits[i] = idctn(Cb_splits[i], type=2)
        Cr_splits[i] = idctn(Cr_splits[i], type=2)
    
    return Y_splits, Cb_splits, Cr_splits