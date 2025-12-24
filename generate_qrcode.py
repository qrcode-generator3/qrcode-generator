from build_data_matrix.encoding import identify_encoding, build_bit_stream
from build_data_matrix.capacity_table import  get_version
from build_data_matrix.error_correction import build_final_codewords
from build_data_matrix.matrix.mask import apply_mask, place_format_info, select_best_mask
from build_data_matrix.matrix.placement import build_base_matrix
from render_data_matrix.render import render_qr



def generate_qrcode(data: str):
    """Generate a QR code image from the input data (fixed EC level 'M')."""
    # Detect best encoding mode for the data
    encoding = identify_encoding(data)

    ec_level = 'M'

    # Choose smallest version that fits the data
    version = get_version(data=data, ec_level=ec_level, encoding_mode=encoding)

    # Build the data bit stream
    bit_stream = build_bit_stream(data=data, encoding=encoding, version=version, ec_level=ec_level)

    # Add error correction and get final codewords
    final_codewords = build_final_codewords(bit_stream, version, ec_level)

    # Create base matrix with reserved areas (patterns, etc.)
    matrix, reserved = build_base_matrix(version=version, final_codewords=final_codewords)

    # Apply masks and pick the best one
    masked_matrix, mask = select_best_mask(matrix, reserved, ec_level=ec_level, version=version, d=data)

    # Write format info (EC level + mask) into reserved areas
    place_format_info(masked_matrix, reserved, mask, ec_level=ec_level)

    # Render and save the QR code image
    render_qr(masked_matrix, scale=10, border=4, filename="a12.png")

