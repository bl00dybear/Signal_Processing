from pathlib import Path

from encodeing_pipeline.utils import load_raw_to_rgb, rgb_to_ycbcr, flatten, encode_with_codes, serialize_compressed
from encodeing_pipeline.split import split_8x8
from encodeing_pipeline.dct import dct_on_splits
from encodeing_pipeline.quantization import quantize
from encodeing_pipeline.huffman import huffman


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

    console.print("[dim blue][*] FLATTENING EACH CHANNEL ... [/dim blue]")
    Y_stream ,Cb_stream ,Cr_stream = flatten(Y_quant, Cb_quant, Cr_quant)
    print(Y_stream.shape)

    codes = huffman(Y_stream ,Cb_stream ,Cr_stream)

    bitstring_Y ,bitstring_Cb ,bitstring_Cr = encode_with_codes(Y_stream ,Cb_stream ,Cr_stream,codes)

    output_path = Path(path).with_suffix('.npz')
    
    console.print("[dim blue][*] SERIALIZING TO NPZ ... [/dim blue]")
    serialize_compressed(bitstring_Y, bitstring_Cb, bitstring_Cr, codes, rgb_image.shape, str(output_path))
    
    console.print(f"\n[bold white][+] BITSTREAM GENERATED. FILE SAVED.[/bold white]")
    console.print(f"[bold green][✓] Compressed file: {output_path}[/bold green]\n")

    console.print("\n[bold white][+] BITSTREAM GENERATED. FILE SAVED.[/bold white]\n")