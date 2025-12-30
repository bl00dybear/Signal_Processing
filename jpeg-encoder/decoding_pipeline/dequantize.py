import numpy as np

Q_JPEG = np.array([
    [16, 11, 10, 16, 24,  40,  51,  61],
    [12, 12, 14, 19, 26,  28,  60,  55],
    [14, 13, 16, 24, 40,  57,  69,  56],
    [14, 17, 22, 29, 51,  87,  80,  62],
    [18, 22, 37, 56, 68,  109, 103, 77],
    [24, 35, 55, 64, 81,  104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])

def dequantize(Y_quant, Cb_quant, Cr_quant, quality_factor):
    num, _, _ = Y_quant.shape
    Q_scaled = Q_JPEG * quality_factor
    
    # Y_dct = np.zeros_like(Y_quant, dtype=float)
    # Cb_dct = np.zeros_like(Cb_quant, dtype=float)
    # Cr_dct = np.zeros_like(Cr_quant, dtype=float)
    
    # for i in range(num):
    #     Y_dct[i] = Y_quant[i] * Q_scaled
    #     Cb_dct[i] = Cb_quant[i] * Q_scaled
    #     Cr_dct[i] = Cr_quant[i] * Q_scaled
    
    # return Y_dct, Cb_dct, Cr_dct

    return Y_quant * Q_scaled, Cb_quant * Q_scaled, Cr_quant * Q_scaled