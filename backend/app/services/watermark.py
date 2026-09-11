"""
DCT-domain invisible watermarking, per the project brief:
- 8x8 image blocks
- mid-frequency DCT coefficients
- redundant embedding across many blocks
- majority-voting extraction (robust to partial corruption/edits)

This is a scaffold: the bit-embedding scheme is implemented and testable,
but has not yet been benchmarked for imperceptibility/robustness — that
belongs in Phase 8/10 (watermark round-trip + tamper-detection tests) per
ImplementationPlan.md.
"""
import numpy as np
import cv2

BLOCK_SIZE = 8
# A mid-frequency coefficient position within the 8x8 DCT block — chosen to
# avoid the DC term (too visible if perturbed) and the highest frequencies
# (too fragile / easily destroyed by compression).
MID_FREQ_POSITION = (4, 3)
EMBED_STRENGTH = 4.0


def _embed_bit_in_block(block: np.ndarray, bit: int) -> np.ndarray:
    dct_block = cv2.dct(block.astype(np.float32))
    coeff = dct_block[MID_FREQ_POSITION]
    # Quantize the coefficient's parity to the target bit.
    quotient = round(coeff / EMBED_STRENGTH)
    if quotient % 2 != bit:
        quotient += 1
    dct_block[MID_FREQ_POSITION] = quotient * EMBED_STRENGTH
    return cv2.idct(dct_block)


def _extract_bit_from_block(block: np.ndarray) -> int:
    dct_block = cv2.dct(block.astype(np.float32))
    coeff = dct_block[MID_FREQ_POSITION]
    quotient = round(coeff / EMBED_STRENGTH)
    return int(quotient % 2)


def embed_content_id(gray_image: np.ndarray, content_id_bits: str) -> np.ndarray:
    """
    Redundantly embeds `content_id_bits` (a string of '0'/'1') across as
    many 8x8 blocks as the image allows, repeating the payload to fill the
    image so extraction can majority-vote each bit position.
    """
    h, w = gray_image.shape
    out = gray_image.copy().astype(np.float32)
    n_bits = len(content_id_bits)
    block_index = 0

    for y in range(0, h - BLOCK_SIZE + 1, BLOCK_SIZE):
        for x in range(0, w - BLOCK_SIZE + 1, BLOCK_SIZE):
            bit = int(content_id_bits[block_index % n_bits])
            block = out[y : y + BLOCK_SIZE, x : x + BLOCK_SIZE]
            out[y : y + BLOCK_SIZE, x : x + BLOCK_SIZE] = _embed_bit_in_block(block, bit)
            block_index += 1

    return np.clip(out, 0, 255).astype(np.uint8)


def extract_content_id(gray_image: np.ndarray, n_bits: int) -> str:
    """
    Extracts `n_bits` using majority voting across all repetitions found in
    the image. Returns the recovered bit string (best-effort — caller is
    responsible for deciding whether the recovered ID is trustworthy, e.g.
    by checking it against a valid content ID format / signature).
    """
    h, w = gray_image.shape
    votes = [[0, 0] for _ in range(n_bits)]  # votes[i] = [count_of_0, count_of_1]
    block_index = 0

    for y in range(0, h - BLOCK_SIZE + 1, BLOCK_SIZE):
        for x in range(0, w - BLOCK_SIZE + 1, BLOCK_SIZE):
            bit_position = block_index % n_bits
            block = gray_image[y : y + BLOCK_SIZE, x : x + BLOCK_SIZE]
            bit = _extract_bit_from_block(block)
            votes[bit_position][bit] += 1
            block_index += 1

    return "".join("1" if v1 > v0 else "0" for v0, v1 in votes)
