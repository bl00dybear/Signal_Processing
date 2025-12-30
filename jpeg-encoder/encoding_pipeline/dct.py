from scipy.fft import dctn, idctn

def dct_on_splits(Y_splits,Cb_splits,Cr_splits):
    num,_,_=Y_splits.shape

    # for i in range (num):
    #     Y_splits[i] = dctn(Y_splits[i],type=2)
    #     Cb_splits[i] = dctn(Cb_splits[i],type=2)
    #     Cr_splits[i] = dctn(Cr_splits[i],type=2)

    return (
            dctn(Y_splits, type=2, axes=(1, 2)),
            dctn(Cb_splits, type=2, axes=(1, 2)),
            dctn(Cr_splits, type=2, axes=(1, 2))
        )
    # return Y_splits,Cb_splits,Cr_splits