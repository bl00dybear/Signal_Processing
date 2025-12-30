import rawpy
import numpy as np

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



def zigzag_scan(block_8x8):
    result = []
    
    zigzag_order = [
        (0,0), (0,1), (1,0), (2,0), (1,1), (0,2),
        (0,3), (1,2), (2,1), (3,0), (4,0), (3,1),
        (2,2), (1,3), (0,4), (0,5), (1,4), (2,3),
        (3,2), (4,1), (5,0), (6,0), (5,1), (4,2),
        (3,3), (2,4), (1,5), (0,6), (0,7), (1,6),
        (2,5), (3,4), (4,3), (5,2), (6,1), (7,0),
        (7,1), (6,2), (5,3), (4,4), (3,5), (2,6),
        (1,7), (2,7), (3,6), (4,5), (5,4), (6,3),
        (7,2), (7,3), (6,4), (5,5), (4,6), (3,7),
        (4,7), (5,6), (6,5), (7,4), (7,5), (6,6),
        (5,7), (6,7), (7,6), (7,7)
    ]
    
    for i, j in zigzag_order:
        result.append(block_8x8[i, j])
    
    return np.array(result)


def flatten(Y_quant, Cb_quant, Cr_quant):
    lenght,_,_=Y_quant.shape

    # print(lenght)

    Y_stream = []
    Cb_stream = []
    Cr_stream = []

    for i in range (lenght):
        Y_stream.extend(zigzag_scan(Y_quant[i]))
        Cb_stream.extend(zigzag_scan(Cb_quant[i]))
        Cr_stream.extend(zigzag_scan(Cr_quant[i]))

    return np.array(Y_stream, dtype=np.int32), np.array(Cb_stream, dtype=np.int32), np.array(Cr_stream, dtype=np.int32)



def encode_with_codes(stream_Y,stream_Cb,stream_Cr, codes):
    bits_Y = ''.join(codes["Y"][int(v)] for v in stream_Y)
    bits_Cb = ''.join(codes["Cb"][int(v)] for v in stream_Cb)
    bits_Cr = ''.join(codes["Cr"][int(v)] for v in stream_Cr)
    return bits_Y, bits_Cb,bits_Cr

def pack_bits_to_bytes(bitstring):
    bit_count = len(bitstring)
    
    padding_needed = (8 - (bit_count % 8)) % 8
    padded_bitstring = bitstring + '0' * padding_needed
    
    byte_data = bytearray()
    for i in range(0, len(padded_bitstring), 8):
        byte = padded_bitstring[i:i+8]
        byte_data.append(int(byte, 2))
    
    return bytes(byte_data), bit_count


def serialize_compressed(bitstring_Y, bitstring_Cb, bitstring_Cr, codes, rgb_image_shape, output_path, quality_factor):
    Y_bytes, Y_bits = pack_bits_to_bytes(bitstring_Y)
    Cb_bytes, Cb_bits = pack_bits_to_bytes(bitstring_Cb)
    Cr_bytes, Cr_bits = pack_bits_to_bytes(bitstring_Cr)
    
    def serialize_codes(codes_dict):
        symbols = np.array(list(codes_dict.keys()), dtype=np.int32)
        code_strs = list(codes_dict.values())
        return symbols, code_strs
    
    Y_symbols, Y_code_strs = serialize_codes(codes["Y"])
    Cb_symbols, Cb_code_strs = serialize_codes(codes["Cb"])
    Cr_symbols, Cr_code_strs = serialize_codes(codes["Cr"])
    
    np.savez_compressed(
        output_path,

        Y_data=np.frombuffer(Y_bytes, dtype=np.uint8),
        Y_bits=np.int32(Y_bits),
        Y_symbols=Y_symbols,
        Y_codes=np.array(Y_code_strs, dtype=object),

        Cb_data=np.frombuffer(Cb_bytes, dtype=np.uint8),
        Cb_bits=np.int32(Cb_bits),
        Cb_symbols=Cb_symbols,
        Cb_codes=np.array(Cb_code_strs, dtype=object),

        Cr_data=np.frombuffer(Cr_bytes, dtype=np.uint8),
        Cr_bits=np.int32(Cr_bits),
        Cr_symbols=Cr_symbols,
        Cr_codes=np.array(Cr_code_strs, dtype=object),

        original_shape=np.array(rgb_image_shape, dtype=np.int32),
        quality_factor=np.float32(quality_factor)
    )