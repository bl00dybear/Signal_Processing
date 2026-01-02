import cv2
import numpy as np

def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    cap.release()
    return frames, fps


def pack_bits_to_bytes(bitstring):
    bit_count = len(bitstring)
    
    padding_needed = (8 - (bit_count % 8)) % 8
    padded_bitstring = bitstring + '0' * padding_needed
    
    byte_data = bytearray()
    for i in range(0, len(padded_bitstring), 8):
        byte = padded_bitstring[i:i+8]
        byte_data.append(int(byte, 2))
    
    return bytes(byte_data), bit_count


def serialize_frame_data(bitstring_Y, bitstring_Cb, bitstring_Cr, codes, quality, shape):
    Y_bytes, Y_bits = pack_bits_to_bytes(bitstring_Y)
    Cb_bytes, Cb_bits = pack_bits_to_bytes(bitstring_Cb)
    Cr_bytes, Cr_bits = pack_bits_to_bytes(bitstring_Cr)
    
    Y_symbols = np.array(list(codes["Y"].keys()), dtype=np.int32)
    Y_codes = list(codes["Y"].values())
    
    Cb_symbols = np.array(list(codes["Cb"].keys()), dtype=np.int32)
    Cb_codes = list(codes["Cb"].values())
    
    Cr_symbols = np.array(list(codes["Cr"].keys()), dtype=np.int32)
    Cr_codes = list(codes["Cr"].values())
    
    return {
        'Y_data': np.frombuffer(Y_bytes, dtype=np.uint8),
        'Y_bits': np.int32(Y_bits),
        'Y_symbols': Y_symbols,
        'Y_codes': np.array(Y_codes, dtype=object),
        'Cb_data': np.frombuffer(Cb_bytes, dtype=np.uint8),
        'Cb_bits': np.int32(Cb_bits),
        'Cb_symbols': Cb_symbols,
        'Cb_codes': np.array(Cb_codes, dtype=object),
        'Cr_data': np.frombuffer(Cr_bytes, dtype=np.uint8),
        'Cr_bits': np.int32(Cr_bits),
        'Cr_symbols': Cr_symbols,
        'Cr_codes': np.array(Cr_codes, dtype=object),
        'quality': quality,
        'shape': shape
    }