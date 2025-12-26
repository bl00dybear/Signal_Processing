import time
import rawpy
import numpy as np

from encodeing_pipeline.split import split_8x8
from encodeing_pipeline.dct import dct_on_splits
from encodeing_pipeline.quantization import quantize

def load_raw_to_rgb(path):
    with rawpy.imread(path) as raw:
        rgb_image = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=True,
            bright=1.0,
            user_sat=None
        )
        return rgb_image
    

# Y = 0.299 * R + 0.587 * G + 0.114 * B
# Cb = -0.1687 * R -0.3313 * G + 0.5 * B + 128
# Cr = 0.5 * R -0.4187 * G -0.0813 * B + 128
def rgb_to_ycbcr(image_rgb):
    xform = np.array([
        [ 0.299,    0.587,    0.114],
        [-0.1687,  -0.3313,   0.5],
        [ 0.5,     -0.4187,  -0.0813]
    ])
    
    ycbcr = image_rgb.dot(xform.T)
    
    return ycbcr




def process_encoding_pipeline(path, console):
    console.print(f"\n[bold cyan][*] SOURCE LOADED:[/bold cyan] [white]{path}[/white]")

    console.print("[dim blue][*] LOADING RAW IMAGE TO RBG ... [/dim blue]")
    rgb_image = load_raw_to_rgb(path)
    print(rgb_image.shape)

    console.print("[dim blue][*] CONVERTING IMAGE IN YCbCr FORMAT ...[/dim blue]")
    ycbcr_image = rgb_to_ycbcr(rgb_image)
    print(ycbcr_image.shape)

    console.print("[dim blue][*] SPLITTING IN 8X8 MATRICES EACH CHANNEL [/dim blue]")
    Y_splits,Cb_splits,Cr_splits = split_8x8(ycbcr_image)
    print(Y_splits.shape)

    console.print("[dim blue][*] DCT ON EACH SPLIT ... [/dim blue]")
    Y_splits_dct,Cb_splits_dct,Cr_splits_dct = dct_on_splits(Y_splits,Cb_splits,Cr_splits)
    print(Y_splits_dct.shape)

    console.print("[dim blue][*] JPEG QUANTIZATION ... [/dim blue]")
    Y_quant, Cb_quant, Cr_quant = quantize(Y_splits_dct,Cb_splits_dct,Cr_splits_dct)
    print(Y_quant.shape)
    
    print()
    console.print("\n[bold white][+] BITSTREAM GENERATED. FILE SAVED.[/bold white]\n")