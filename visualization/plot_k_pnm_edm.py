import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import rc

rc('text', usetex=True)

fig_width = 3.5

table = pd.read_csv('../out/plotting_data_for_analysis.csv')
df = pd.DataFrame(table)

df = df.sort_values(by=['k_pnm'])
df.index = df.k_pnm

fig1, ax1 = plt.subplots(figsize=(fig_width, fig_width), tight_layout=True)
ax1 = df.plot(x='k_pnm', y='k_edm', style='o', label='artificial', legend=False, zorder=1,
              ax=ax1, alpha=0.3)

k_min = 5.e-14
k_max = 5.e-10

ax1.set_xlim(k_min, k_max)
ax1.set_ylim(k_min, k_max)

ax1.set_xlabel('$K_{pnm}, m^2$')
ax1.set_ylabel('$K_{edm}, m^2$')

plt.gca().set_aspect('equal', adjustable='box')
plt.plot([k_min, k_max], [k_min, k_max], label='diagonal', zorder=2, alpha=0.7)

plt.scatter(1.067776E-11, 1.013048E-11, c="r", marker='s', label='(a)', zorder=3, s=50)
plt.scatter(2.298116E-13, 1.889883E-13, c="cyan", marker='s', label='(b)', zorder=3, s=50)
plt.scatter(4.194141E-10, 3.555365E-10, c="y", marker='s', label='(c)', zorder=3, s=50)
plt.scatter(3.622896E-12, 1.487646E-12, c="m", marker='s', label='(d)', zorder=3, s=50)

plt.legend(fancybox=True, framealpha=1)

plt.yscale("log")
plt.xscale("log")

plt.savefig('../out/k_pnm_edm.pdf', format="pdf", bbox_inches='tight')

# plt.show()
