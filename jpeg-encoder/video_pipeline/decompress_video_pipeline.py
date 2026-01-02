import numpy as np
from pathlib import Path
import cv2
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from decoding_pipeline.huffman import huffman_decode_all
from decoding_pipeline.inverse_split import unflatten, reconstruct_from_blocks
from decoding_pipeline.dequantize import dequantize
from decoding_pipeline.inverse_dct import idct_on_splits
from decoding_pipeline.utils import merge_channels, ycbcr_to_rgb


def decompress_frame(frame_data):
    Y_stream, Cb_stream, Cr_stream = huffman_decode_all(frame_data)
    
    num_blocks = len(Y_stream) // 64
    
    Y_blocks, Cb_blocks, Cr_blocks = unflatten(Y_stream, Cb_stream, Cr_stream, num_blocks)
    
    Y_dequant, Cb_dequant, Cr_dequant = dequantize(Y_blocks, Cb_blocks, Cr_blocks, frame_data['quality'])
    
    Y_idct, Cb_idct, Cr_idct = idct_on_splits(Y_dequant, Cb_dequant, Cr_dequant)
    
    original_height, original_width = frame_data['shape'][0], frame_data['shape'][1]
    Y_final, Cb_final, Cr_final = reconstruct_from_blocks(Y_idct, Cb_idct, Cr_idct, original_height, original_width)
    Y_final = Y_final + 128
    
    ycbcr_image = merge_channels(Y_final, Cb_final, Cr_final)
    
    rgb_image = ycbcr_to_rgb(ycbcr_image)
    
    return rgb_image


def decompress_video_pipeline(video_path, console):
    compressed_data = np.load(video_path, allow_pickle=True)
    
    num_frames = int(compressed_data['num_frames'])
    fps = float(compressed_data['fps'])
    frames_data = compressed_data['frames']
    
    decompressed_frames = []
    
    console.print(f"[dim]Decompressing frame 1/{num_frames}[/dim]")
    frame_rgb = decompress_frame(frames_data[0])
    decompressed_frames.append(frame_rgb)
    
    def process_frame(i, frame_data):
        console.print(f"[dim]Decompressing frame {i}/{num_frames}[/dim]")
        frame_rgb = decompress_frame(frame_data)
        return i-1, frame_rgb
    
    results = [None] * (num_frames - 1)
    
    max_workers = os.cpu_count()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_frame, i+1, frame_data): i 
                   for i, frame_data in enumerate(frames_data[1:])}
        for future in as_completed(futures):
            idx, frame_rgb = future.result()
            results[idx] = frame_rgb
    
    decompressed_frames.extend(results)
    
    output_path = Path(video_path).stem + '-decompressed.mp4'
    output_path = Path(video_path).parent / output_path
    
    height, width = decompressed_frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    for frame in decompressed_frames:
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
    
    out.release()
    
    console.print(f"\n[bold white][+] VIDEO DECOMPRESSED: {output_path}[/bold white]")
