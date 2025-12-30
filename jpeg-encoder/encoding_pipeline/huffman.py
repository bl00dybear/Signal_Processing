import heapq


def counter(stream):
    freq={}

    for i in range(len(stream)):
        if stream[i] not in freq:
            freq[stream[i]] = 1
        else:
            freq[stream[i]] += 1

    return freq

def build_huffman_tree(freq):
    index = 0
    heap = []
    for num, cnt in freq.items():
        heap.append((cnt, index, num))
        index += 1    
        
    heapq.heapify(heap)

    while len(heap) > 1:
        f1, _, t1 = heapq.heappop(heap)
        f2, _, t2 = heapq.heappop(heap)
        parent = (t1, t2)
        heapq.heappush(heap, (f1 + f2, index, parent))
        index += 1

    return heap[0][2]

def build_codes(tree):
    codes = {}
    
    def dfs(node, path):
        if isinstance(node, tuple):
            dfs(node[0], path + "0")
            dfs(node[1], path + "1")
        else:
            codes[int(node)] = path if path else "0"
    
    dfs(tree, "")
    return codes


def huffman(Y_stream ,Cb_stream ,Cr_stream):
    Y_freq = counter(Y_stream)
    Cb_freq = counter(Cb_stream)
    Cr_freq = counter(Cr_stream)

    Y_tree = build_huffman_tree(Y_freq)
    Cb_tree = build_huffman_tree(Cb_freq)
    Cr_tree = build_huffman_tree(Cr_freq)

    Y_codes = build_codes(Y_tree)
    Cb_codes = build_codes(Cb_tree)
    Cr_codes = build_codes(Cr_tree)

    return {"Y": Y_codes, "Cb": Cb_codes, "Cr": Cr_codes}
