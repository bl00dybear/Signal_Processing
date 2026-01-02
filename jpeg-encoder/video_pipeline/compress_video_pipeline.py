import numpy as np
from pathlib import Path
import os

from video_pipeline.utils import extract_frames, serialize_frame_data

from encoding_pipeline.utils import rgb_to_ycbcr
from encoding_pipeline.split import split_8x8
from encoding_pipeline.dct import dct_on_splits
from encoding_pipeline.quantization import quantize, binary_search_quality
from encoding_pipeline.huffman import huffman
from encoding_pipeline.utils import flatten, encode_with_codes



def compress_frame(frame,console,calc_quality=0,mse_threshold=1,quality=1.0):
    ycbcr = rgb_to_ycbcr(frame)
    
    Y_splits, Cb_splits, Cr_splits = split_8x8(ycbcr)
    
    Y_dct, Cb_dct, Cr_dct = dct_on_splits(Y_splits, Cb_splits, Cr_splits)
    
    if calc_quality:
        quality = binary_search_quality(Y_dct, Cb_dct, Cr_dct, mse_threshold, console)
    
    Y_quant, Cb_quant, Cr_quant = quantize(Y_dct, Cb_dct, Cr_dct, quality)
    
    Y_stream, Cb_stream, Cr_stream = flatten(Y_quant, Cb_quant, Cr_quant)
    
    codes = huffman(Y_stream, Cb_stream, Cr_stream)
    
    bitstring_Y, bitstring_Cb, bitstring_Cr = encode_with_codes(Y_stream, Cb_stream, Cr_stream, codes)
    
    return bitstring_Y, bitstring_Cb, bitstring_Cr,codes,quality,frame.shape


def compress_video_pipeline(video_path, console,mse_threshold):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    frames, fps = extract_frames(video_path)

    compressed_frames = []
    
    console.print(f"[dim]Processing frame 1/{len(frames)}[/dim]")
    bitstring_Y, bitstring_Cb, bitstring_Cr, codes, quality, shape = compress_frame(
        frames[0], console, calc_quality=1, mse_threshold=mse_threshold
    )

    frame_data = serialize_frame_data(bitstring_Y, bitstring_Cb, bitstring_Cr, codes, quality, shape)
    compressed_frames.append(frame_data)
    
    console.print(f"[bold green][*] Quality factor: {quality:.2f}[/bold green]")
    
    def process_frame(i, frame):
        console.print(f"[dim]Processing frame {i}/{len(frames)}[/dim]")
        bitstring_Y, bitstring_Cb, bitstring_Cr, codes, _, shape = compress_frame(
            frame, console, calc_quality=0, quality=quality
        )
        frame_data = serialize_frame_data(bitstring_Y, bitstring_Cb, bitstring_Cr, codes, quality, shape)
        return i-1, frame_data
    
    results = [None] * (len(frames) - 1)

    max_workers=os.cpu_count()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_frame, i+1, frame): i 
                   for i, frame in enumerate(frames[1:])}
        for future in as_completed(futures):
            idx, frame_data = future.result()
            results[idx] = frame_data
    
    compressed_frames.extend(results)
    
    output_path = Path(video_path).with_suffix('.npz')
    np.savez_compressed(
        output_path,
        num_frames=len(compressed_frames),
        fps=fps,
        frames=compressed_frames
    )
    
    console.print(f"\n[bold white][+] VIDEO COMPRESSED: {output_path}[/bold white]")
    return str(output_path)