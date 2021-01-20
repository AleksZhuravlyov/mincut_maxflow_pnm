import sys
import os
import numpy as np
import openpnm as op
import porespy as ps
import re

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../'))
from computations.calculate_flows import calculate_flows
from max_radius.calculate_max_radius import calculate_max_radius


# This function allows to flip void/rock phases if needed
def flip_values(data, val1, val2):
    data = np.where(data == val1, -999.25, data)
    data = np.where(data == val2, val1, data)
    data = np.where(data == -999.25, val2, data)
    return data


# This function allows exporting and processing segmenting image from raw file
def read_raw_file(base_path, mhd_file_name):
    dims = list()
    voxel_sizes = list()
    raw_file_name = str()
    with open(base_path + '/' + mhd_file_name, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            words = re.split(' = | |\n', line)
            words.pop(-1)
            key = words.pop(0)
            if key == 'DimSize':
                for word in words:
                    dims.append(int(word))
                dims.reverse()
            elif key == 'ElementSize':
                for word in words:
                    voxel_sizes.append(float(word))
                voxel_sizes.reverse()
            elif key == 'ElementDataFile':
                raw_file_name = str(words.pop(0))

    with open(base_path + '/' + raw_file_name, 'rb') as raw_file:
        data = list(raw_file.read())

    image = np.reshape(np.array(data, dtype=bool), (dims[0], dims[1], dims[2]))
    image = np.transpose(image)
    image = flip_values(image, 0, 1).astype(bool)

    case_name = os.path.splitext(os.path.basename(raw_file_name))[0]

    return image, dims, voxel_sizes, case_name


def extract_pn(image, voxel_size, case_name):
    # Runs pore network extraction algorithm
    net = ps.networks.snow(image, voxel_size=voxel_size)
    return net


if __name__ == '__main__':
    im, dims, voxel_sizes, case_name = read_raw_file('../real_samples', 'gambier_512.mhd')
    net = extract_pn(image=im, voxel_size=voxel_sizes[0], case_name=case_name)
    flow_params, min_cut = calculate_flows(net)
    input_output_im = np.zeros_like(im, dtype=int)
    input_output_im[0, :, :] = im[0, :, :]
    input_output_im[dims[0] - 1, :, :] = im[dims[0] - 1, :, :] * 2
    calculate_max_radius(im, voxel_sizes[0], input_output_im, case_name + '__')
