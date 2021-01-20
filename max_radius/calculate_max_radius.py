# MIT License
#
# Copyright (c) 2020 Aleksandr Zhuravlyov and Zakhar Lanets
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import numpy as np
from scipy import ndimage

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../'))
from max_radius.max_radius import bool_shooting_method, Max_radius


def calculate_max_radius(segmented_im, voxel_size, input_output_im, file_name):
    # calculate distance map
    distance_map_im = ndimage.distance_transform_edt(segmented_im)
    distance_map_im *= voxel_size    

    # calculate max radius
    input_im = np.where(input_output_im == 1, 1, 0)
    output_im = np.where(input_output_im == 2, 1, 0)
    max_radius = Max_radius(distance_map_im, input_im, output_im, voxel_size=voxel_size)
    result = bool_shooting_method(max_radius.is_propagated, init_x=1.e-6,
                                  init_dx=1.e-6, min_dx=1.e-9)

    print('threshold, accuracy', result)

    np.savetxt(file_name + '_max_radius.txt', [result[0]])

    return result
