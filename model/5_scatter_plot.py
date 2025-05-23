import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import scienceplots
from matplotlib.patches import Circle

_color_line1 = "#DF6D2D"
_color_line2 = "#4B5945"
_color_area = "#D9EAFD"


plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "serif",
    }
)
plt.style.use(["science", "ieee"])

_factor = 2.2
_fontsize = 14


def set_x_ticklabels_function(axis):
    x_points = [0, 6, 12, 18, 24, 30, 36]
    axis.set_xticks(x_points)
    axis.set_xticklabels(
        ["01-2021", "07-2021", "01-2022", "07-2022", "01-2023", "07-2023", "01-2024"]
    )
    return


plt.style.use(["ieee"])
plt.rcParams["xtick.labelsize"] = _fontsize
plt.rcParams["ytick.labelsize"] = _fontsize

_time = "20250218_2133"

###############################################################################

fig, ax = plt.subplots(figsize=(_factor * 2.5, _factor * 1.5))

data = pd.read_excel("_RESULTS_sensitivity.xlsx")

_x = data['Price increase (in %)']
_y = data['Suppressed demand (in %)']
_x1 = data['Profit increase (in %)']

ax.scatter(_x, _y, marker='o', color='#003092', s=8, label=r'Price', zorder=2)
ax.scatter(_x1, _y, marker='o', color='#B7B1F2', s=8, label=r'Revenue')


ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1, lw=0.5)
ax.grid(which="major", axis="x", color="#758D99", alpha=0.2, zorder=1, lw=0.5)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

ax.set_ylabel(r"Suppressed demand share (in \%)", fontsize=_fontsize)
ax.set_xlabel(r"Relative increase (in \%)", fontsize=_fontsize)

_legend = ax.legend(
    loc="center",
    facecolor="white",
    fontsize=14,
    handlelength=0.5,
    handletextpad=0.25,
    ncol=2,
    borderpad=0.35,
    columnspacing=0.75,
    edgecolor="black",
    frameon=True,
    bbox_to_anchor=(0.5, 0.9),
    shadow=False,
    framealpha=1,
    markerscale=2
)

ax.text(x=10, y=-1., s=r"a", va='center', ha='center', fontsize=12, color='black')
circle = Circle((10, -1.), radius=2.75, edgecolor='black', facecolor='none', linewidth=0.75)
ax.add_patch(circle)

ax.text(x=80, y=-35.5, s='b', va='center', ha='center', fontsize=12)
circle = Circle((80, -35.5), radius=2.75, edgecolor='black', facecolor='none', linewidth=0.75)
ax.add_patch(circle)

ax.text(x=205, y=-37.5, s='c', va='center', ha='center', fontsize=12)
circle = Circle((205, -37.5), radius=2.75, edgecolor='black', facecolor='none', linewidth=0.75)
ax.add_patch(circle)

ax.text(x=205, y=-1, s='d', va='center', ha='center', fontsize=12)
circle = Circle((205, -1), radius=2.75, edgecolor='black', facecolor='none', linewidth=0.75)
ax.add_patch(circle)

plt.tight_layout()
ax.set_xlim([-10, 210])
ax.set_ylim([-42, 2])

_col = '#A53860'
ax.plot(54, -25.92, marker = '*', ms = 10, color=_col)
ax.plot(14.08, -25.92, marker = '*', ms = 10, color=_col)

ax.text(x=14.08+(54-14.08)/2, y=-25.92, s='e', va='center', ha='center', fontsize=12, color=_col)
_x=14.08+(54-14.08)/2
circle = Circle((_x, -25.92), radius=2.75, edgecolor=_col, facecolor='none', linewidth=0.75)
ax.add_patch(circle)

fig.savefig("result/" + _time + "/RESULTS_scatterplot.pdf", dpi=1000)
