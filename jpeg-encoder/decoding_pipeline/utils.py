import numpy as np

def ycbcr_to_rgb(image_ycbcr):
    xform = np.array([
        [1.0,     0.0,      1.402],
        [1.0,    -0.34414, -0.71414],
        [1.0,     1.772,    0.0]
    ])
    
    rgb = image_ycbcr.dot(xform.T)
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    
    return rgb


def merge_channels(Y, Cb, Cr):
    height, width = Y.shape
    ycbcr = np.zeros((height, width, 3))
    
    ycbcr[:, :, 0] = Y
    ycbcr[:, :, 1] = Cb
    ycbcr[:, :, 2] = Cr
    
    return ycbcr