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


def bool_shooting_method(bool_function, init_x, init_dx, min_dx):
    ind = 0
    y_curr = bool_function(init_x, ind)

    y_prev = y_curr
    x = init_x
    if y_curr:
        dx = abs(init_dx)
    else:
        dx = -abs(init_dx)

    while True:
        x += dx
        y_prev = y_curr
        ind += 1
        print('bool shooting ind: dx', ind, ': ', dx)
        y_curr = bool_function(x, ind)
        if y_curr != y_prev:
            dx /= -2.
        if abs(dx) < abs(min_dx):
            break

    return x, abs(dx)


class Max_radius:
    def __init__(s, distance_map_im, input_im, output_im, voxel_size=1.e-6):
        s.distance_map_im = distance_map_im
        s.input_im = input_im
        s.output_im = output_im
        s.save_paraview = save_paraview
        s.voxel_size = voxel_size

    def is_propagated(s, threshold, ind=0):
        mask = np.where(s.distance_map_im > threshold, 1, 0)
        propagation = ndimage.binary_propagation(input=s.input_im, mask=mask).astype(np.int)
        return bool(np.count_nonzero(propagation[np.nonzero(s.output_im)]))
