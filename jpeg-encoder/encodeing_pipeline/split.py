import numpy as np

def pad_height(ycbcr_img,h_pad):
    h,_,_=ycbcr_img.shape
    last_row = ycbcr_img[h-1:h,:,:]
    pad = last_row

    for _ in range(h_pad-1):
        pad = np.vstack([pad,last_row])

    ycbcr_img = np.vstack([ycbcr_img,pad])

    return ycbcr_img

def pad_width(ycbcr_img,w_pad):
    _,w,_=ycbcr_img.shape
    last_col = ycbcr_img[:,w-1:w,:]
    pad = last_col

    for _ in range(w_pad-1):
        pad = np.hstack([pad,last_col])

    ycbcr_img = np.hstack([ycbcr_img,pad])

    return ycbcr_img


def split_8x8(ycbcr_img):
    h,w,_=ycbcr_img.shape

    h_pad = (8 - (h % 8)) % 8
    w_pad = (8 - (w % 8)) % 8
    if h_pad:
        ycbcr_img = pad_height(ycbcr_img, h_pad)
    if w_pad:
        ycbcr_img = pad_width(ycbcr_img, w_pad)

    h,w,_=ycbcr_img.shape

    Y_mat = ycbcr_img[:,:,0].astype(float)-128
    Cb_mat = ycbcr_img[:,:,1]
    Cr_mat = ycbcr_img[:,:,2]

    Y_splits = np.zeros((h//8*w//8,8,8))
    Cb_splits = np.zeros((h//8*w//8,8,8))
    Cr_splits = np.zeros((h//8*w//8,8,8))

    for i in range (h//8):
        for j in range (w//8):

            for ii in range(8):
                for jj in range(8):
                    Y_splits[i*(w//8)+j,ii,jj] = Y_mat[i*8+ii,j*8+jj]
                    Cb_splits[i*(w//8)+j,ii,jj] = Cb_mat[i*8+ii,j*8+jj]
                    Cr_splits[i*(w//8)+j,ii,jj] = Cr_mat[i*8+ii,j*8+jj]


    return Y_splits,Cb_splits,Cr_splits