import numpy as np

Q_JPEG= np.array([
    [16, 11, 10, 16, 24,  40,  51,  61],
    [12, 12, 14, 19, 26,  28,  60,  55],
    [14, 13, 16, 24, 40,  57,  69,  56],
    [14, 17, 22, 29, 51,  87,  80,  62],
    [18, 22, 37, 56, 68,  109, 103, 77],
    [24, 35, 55, 64, 81,  104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])


def quantize(Y_dct, Cb_dct, Cr_dct):
    num, _, _ = Y_dct.shape
    
    Y_quant = np.zeros_like(Y_dct)
    Cb_quant = np.zeros_like(Cb_dct)
    Cr_quant = np.zeros_like(Cr_dct)
    
    for i in range(num):
        Y_quant[i] = Q_JPEG * np.round(Y_dct[i]/Q_JPEG) 
        Cb_quant[i] = Q_JPEG * np.round(Cb_dct[i] / Q_JPEG)
        Cr_quant[i] = Q_JPEG * np.round(Cr_dct[i] / Q_JPEG)
    
    return Y_quant, Cb_quant, Cr_quant