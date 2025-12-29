import numpy as np


def unpack_bits_from_bytes(byte_data, bit_count):
    bitstring = ''.join(format(byte, '08b') for byte in byte_data)
    return bitstring[:bit_count]


def huffman_decode(bitstring, symbols, codes):
    code_to_symbol = {}
    for i, symbol in enumerate(symbols):
        code_to_symbol[codes[i]] = symbol
    
    decoded_stream = []
    current_code = ""
    
    for bit in bitstring:
        current_code += bit
        if current_code in code_to_symbol:
            decoded_stream.append(code_to_symbol[current_code])
            current_code = ""
    
    return np.array(decoded_stream, dtype=np.int32)


def huffman_decode_all(npz_data):
    Y_bitstring = unpack_bits_from_bytes(npz_data['Y_data'], int(npz_data['Y_bits']))
    Cb_bitstring = unpack_bits_from_bytes(npz_data['Cb_data'], int(npz_data['Cb_bits']))
    Cr_bitstring = unpack_bits_from_bytes(npz_data['Cr_data'], int(npz_data['Cr_bits']))
    
    Y_stream = huffman_decode(Y_bitstring, npz_data['Y_symbols'], npz_data['Y_codes'])
    Cb_stream = huffman_decode(Cb_bitstring, npz_data['Cb_symbols'], npz_data['Cb_codes'])
    Cr_stream = huffman_decode(Cr_bitstring, npz_data['Cr_symbols'], npz_data['Cr_codes'])
    
    return Y_stream, Cb_stream, Cr_stream