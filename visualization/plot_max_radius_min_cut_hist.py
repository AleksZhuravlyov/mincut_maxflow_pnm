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

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

rc('text', usetex=True)

bead_pack = np.loadtxt('../out/bead_pack_512_min_cut_radii.txt') * 1.e+6
bead_pack_max_radius = np.loadtxt('../out/bead_pack_512_max_radius.txt') * 1.e+6

castle = np.loadtxt('../out/castle_512_min_cut_radii.txt') * 1.e+6
castle_max_radius = np.loadtxt('../out/castle_512_max_radius.txt') * 1.e+6

gambier = np.loadtxt('../out/gambier_512_min_cut_radii.txt') * 1.e+6
gambier_max_radius = np.loadtxt('../out/gambier_512_max_radius.txt') * 1.e+6

lrc32 = np.loadtxt('../out/lrc32_512_min_cut_radii.txt') * 1.e+6
lrc32_max_radius = np.loadtxt('../out/lrc32_512_max_radius.txt') * 1.e+6

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(3.8, 3.8))

ax1.hist(bead_pack, bins=20, alpha=0.5, label='PDF')
ax11 = ax1.twinx()
ax11.hist(bead_pack, bins=40, density=True, histtype='step', cumulative=True, label='CDF')
x1 = np.array([bead_pack_max_radius, bead_pack_max_radius])
y1 = np.array(ax1.get_ylim())
ax1.plot(x1, y1, lw=4, label='critical radius')
ax1.set_title('(a)')
ax1.set_ylim(y1 * 1)

ax2.hist(castle, bins=10, alpha=0.5)
ax21 = ax2.twinx()
ax21.hist(castle, bins=20, density=True, histtype='step', cumulative=True)
x2 = np.array([castle_max_radius, castle_max_radius])
y2 = np.array(ax2.get_ylim()) * 2.2
ax2.plot(x2, y2 * 0.48, lw=4)
ax2.set_title('(b)')
ax2.set_ylim(y2 * 0.45)

ax3.hist(lrc32, bins=15, alpha=0.5)
ax31 = ax3.twinx()
ax31.hist(lrc32, bins=30, density=True, histtype='step', cumulative=True)
x3 = np.array([lrc32_max_radius, lrc32_max_radius])
y3 = np.array(ax3.get_ylim())
ax3.plot(x3, y3, lw=4)
ax3.set_title('(c)')
ax3.set_ylim(y3 * 1)

ax4.hist(gambier, bins=20, alpha=0.5)
ax41 = ax4.twinx()
ax41.hist(gambier, bins=40, density=True, histtype='step', cumulative=True)
x4 = np.array([gambier_max_radius, gambier_max_radius])
y4 = np.array(ax4.get_ylim())
ax4.plot(x4, y4, lw=4)
ax4.set_title('(d)')
ax4.set_ylim(y4 * 1)

fig.text(-0.02, 0.5, 'throats number', va='center', rotation='vertical')
fig.text(0.99, 0.5, 'throats cumulative distribution', va='center', rotation='vertical')
fig.text(0.5, 0.075, 'throats radius, ' + r'$\mu m$', ha='center')

fig.tight_layout(pad=0.7)

fig.subplots_adjust(bottom=0.165)

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax11.get_legend_handles_labels()
fig.legend(handles1 + handles2, labels1 + labels2, loc=(0.115, 0.008), ncol=3)

plt.savefig('../out/max_radius_min_cut_hist.pdf', format='pdf', bbox_inches='tight')

# plt.show()
