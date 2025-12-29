import numpy as np
from pathlib import Path
from PIL import Image


from decoding_pipeline.huffman import huffman_decode_all
from decoding_pipeline.inverse_split import unflatten, reconstruct_from_blocks
from decoding_pipeline.inverse_dct import idct_on_splits
from decoding_pipeline.utils import merge_channels, ycbcr_to_rgb
from decoding_pipeline.dequantize import dequantize

def process_decoding_pipeline(path, console):
    console.print(f"\n[bold cyan][*] LOADING COMPRESSED FILE:[/bold cyan] [white]{path}[/white]")
    npz_data = np.load(path, allow_pickle=True)
    original_shape = tuple(npz_data['original_shape'])
    original_height, original_width = original_shape[0], original_shape[1]
    
    console.print("[dim blue][*] HUFFMAN DECODING ... [/dim blue]")
    Y_stream, Cb_stream, Cr_stream = huffman_decode_all(npz_data)
    num_blocks = len(Y_stream) // 64
    
    console.print("[dim blue][*] UNFLATTENING STREAMS ... [/dim blue]")
    Y_blocks, Cb_blocks, Cr_blocks = unflatten(Y_stream, Cb_stream, Cr_stream, num_blocks)
    
    console.print("[dim blue][*] DEQUANTIZING ... [/dim blue]")
    Y_dequant, Cb_dequant, Cr_dequant = dequantize(Y_blocks, Cb_blocks, Cr_blocks)
    

    console.print("[dim blue][*] INVERSE DCT ... [/dim blue]")
    Y_idct, Cb_idct, Cr_idct = idct_on_splits(Y_dequant, Cb_dequant, Cr_dequant)    
    
    console.print("[dim blue][*] RECONSTRUCTING IMAGE ... [/dim blue]")
    Y_final, Cb_final, Cr_final = reconstruct_from_blocks(Y_idct, Cb_idct, Cr_idct, original_height, original_width)
    Y_final = Y_final + 128
    
    console.print("[dim blue][*] MERGING CHANNELS ... [/dim blue]")
    ycbcr_image = merge_channels(Y_final, Cb_final, Cr_final)
    
    console.print("[dim blue][*] CONVERTING TO RGB ... [/dim blue]")
    rgb_image = ycbcr_to_rgb(ycbcr_image)
    output_path = Path(path).with_suffix('.png')


    img = Image.fromarray(rgb_image)
    img.save(str(output_path))
    
    console.print(f"\n[bold white][+] DECODING COMPLETE.[/bold white]")