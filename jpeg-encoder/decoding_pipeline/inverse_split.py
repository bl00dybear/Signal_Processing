import numpy as np

def inverse_zigzag_scan(zigzag_array):
    block_8x8 = np.zeros((8, 8))
    
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
    
    for idx, (i, j) in enumerate(zigzag_order):
        block_8x8[i, j] = zigzag_array[idx]
    
    return block_8x8


def unflatten(Y_stream, Cb_stream, Cr_stream, num_blocks):
    Y_blocks = []
    Cb_blocks = []
    Cr_blocks = []
    
    for i in range(num_blocks):
        Y_blocks.append(inverse_zigzag_scan(Y_stream[i*64:(i+1)*64]))
        Cb_blocks.append(inverse_zigzag_scan(Cb_stream[i*64:(i+1)*64]))
        Cr_blocks.append(inverse_zigzag_scan(Cr_stream[i*64:(i+1)*64]))
    
    return np.array(Y_blocks), np.array(Cb_blocks), np.array(Cr_blocks)


def remove_padding(image, original_height, original_width):
    return image[:original_height, :original_width]


def reconstruct_from_blocks(Y_blocks, Cb_blocks, Cr_blocks, original_height, original_width):
    blocks_per_row = (original_width + 7) // 8
    
    Y_reconstructed = np.zeros((original_height + (8-original_height%8)%8, 
                                 original_width + (8-original_width%8)%8))
    Cb_reconstructed = np.zeros_like(Y_reconstructed)
    Cr_reconstructed = np.zeros_like(Y_reconstructed)
    
    for i, block in enumerate(Y_blocks):
        row = (i//blocks_per_row)*8
        col = (i%blocks_per_row)*8
        Y_reconstructed[row:row+8, col:col+8] = block
        Cb_reconstructed[row:row+8, col:col+8] = Cb_blocks[i]
        Cr_reconstructed[row:row+8, col:col+8] = Cr_blocks[i]
    
    Y_reconstructed = remove_padding(Y_reconstructed, original_height, original_width)
    Cb_reconstructed = remove_padding(Cb_reconstructed, original_height, original_width)
    Cr_reconstructed = remove_padding(Cr_reconstructed, original_height, original_width)
    
    return Y_reconstructed, Cb_reconstructed, Cr_reconstructed