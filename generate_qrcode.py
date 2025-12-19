from build_data_matrix.encoding import identify_encoding
from build_data_matrix.capacity_table import  get_version

def generate_qrcode(data: str):
    encoding = identify_encoding(data) # returns int
    version = get_version(data, 3) # returns int

    # generate the matrix
    # render the matrix

