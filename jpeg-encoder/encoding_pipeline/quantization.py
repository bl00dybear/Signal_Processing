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


def quantize(Y_dct, Cb_dct, Cr_dct, quality_factor):
    num, _, _ = Y_dct.shape

    Q_jpeg = Q_JPEG*quality_factor
    
    # Y_quant = np.zeros_like(Y_dct)
    # Cb_quant = np.zeros_like(Cb_dct)
    # Cr_quant = np.zeros_like(Cr_dct)
    
    # for i in range(num):
    #     Y_quant[i] = np.round(Y_dct[i]/Q_jpeg) 
    #     Cb_quant[i] = np.round(Cb_dct[i] / Q_jpeg)
    #     Cr_quant[i] = np.round(Cr_dct[i] / Q_jpeg)
    
    # return Y_quant, Cb_quant, Cr_quant

    return np.round(Y_dct / Q_jpeg), np.round(Cb_dct / Q_jpeg), np.round(Cr_dct / Q_jpeg)


def calculate_mse_from_dct(Y_dct, Cb_dct, Cr_dct, Q_scaled):
    Y_q = np.round(Y_dct / Q_scaled)
    Cb_q = np.round(Cb_dct / Q_scaled)
    Cr_q = np.round(Cr_dct / Q_scaled)
    
    Y_rec = Y_q * Q_scaled
    Cb_rec = Cb_q * Q_scaled
    Cr_rec = Cr_q * Q_scaled
    
    mse_Y = np.mean((Y_dct - Y_rec) ** 2)
    mse_Cb = np.mean((Cb_dct - Cb_rec) ** 2)
    mse_Cr = np.mean((Cr_dct - Cr_rec) ** 2)
    
    return mse_Y * 0.6 + mse_Cb * 0.2 + mse_Cr * 0.2


def binary_search_quality(Y_dct, Cb_dct, Cr_dct, mse_threshold, console):
    low, high = 0.01, 100.0
    best_factor = 1.0
    epsilon = 0.01
    
    while high - low > epsilon:
        mid = (low + high) / 2
        
        Q_scaled = Q_JPEG * mid
        mse = calculate_mse_from_dct(Y_dct, Cb_dct, Cr_dct, Q_scaled)
        
        console.print(f"[dim]Factor={mid:.2f}, MSE={mse:.4f}[/dim]")
        
        if mse <= mse_threshold:
            best_factor = mid
            low = mid
        else:
            high = mid
    
    return best_factor