import heapq
import os
from collections import defaultdict, Counter


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def calculate_frequency(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    frequency = Counter(text)
    return frequency


def build_huffman_tree(frequency):
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue);
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(priority_queue, merged)

    return priority_queue[0]


def generate_huffman_codes(node, code='', code_map={}):
    if node is None:
        return
    if node.char is not None:
        code_map[node.char] = code
    generate_huffman_codes(node.left, code + '0', code_map)
    generate_huffman_codes(node.right, code + '1', code_map)
    return code_map


def encode_file(input_file, output_file, huffman_codes):
    with open(input_file, 'r') as file:
        text = file.read()

    encoded_text = ''.join(huffman_codes[char] for char in text)

    # Pad encoded text to make it byte-aligned
    padded_encoded_text = encoded_text + '0' * ((8 - len(encoded_text) % 8) % 8)

    # Convert binary string to bytes
    byte_array = bytearray(int(padded_encoded_text[i:i + 8], 2) for i in range(0, len(padded_encoded_text), 8))

    # Write to compressed file
    with open(output_file, 'wb') as file:
        file.write(bytes(byte_array))


def decode_file(compressed_file, output_file, root):
    with open(compressed_file, 'rb') as file:
        byte_data = file.read()

    # Convert bytes to binary string
    binary_string = ''.join(format(byte, '08b') for byte in byte_data)

    # Traverse the Huffman tree to decode the text
    decoded_text = ''
    current_node = root
    for bit in binary_string:
        current_node = current_node.left if bit == '0' else current_node.right

        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = root

    # Write to decompressed file
    with open(output_file, 'w') as file:
        file.write(decoded_text)


if __name__ == '__main__':
    input_file = '/Users/apple/Desktop/Python/Python Project & CP/File Compressor/output-onlinefiletools.txt'
    compressed_file = 'compressed.bin'
    decompressed_file = 'decompressed.txt'

    # Frequency calculation and tree building
    frequency = calculate_frequency(input_file)
    huffman_tree_root = build_huffman_tree(frequency)

    # Generate codes and encode
    huffman_codes = generate_huffman_codes(huffman_tree_root)
    encode_file(input_file, compressed_file, huffman_codes)

    # Decompress to verify
    decode_file(compressed_file, decompressed_file, huffman_tree_root)

    print("Compression and decompression complete!")
