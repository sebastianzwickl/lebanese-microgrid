import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# import scienceplots
import matplotlib as mpl
from statsmodels.graphics.tsaplots import plot_acf
from matplotlib.collections import PolyCollection

_color_demand = "#024CAA"
_color_price = "#EB8317"


def set_x_ticklabels_function(axis):
    x_points = [0, 6, 12, 18, 24, 30, 36]
    axis.set_xticks(x_points)
    axis.set_xticklabels(
        ["01|2021", "07|2021", "01|2022", "07|2022", "01|2023", "07|2023", "01|2024"]
    )
    for point in x_points[::2]:
        axis.axvline(point, linestyle="--", color="gray", zorder=0)
    return


# plt.style.use(['no-latex'])
plt.style.use("classic")
plt.rcParams["figure.figsize"] = [8, 4]
plt.rcParams["xtick.labelsize"] = 11
plt.rcParams["ytick.labelsize"] = 11

data = pd.read_excel("../model/1_sorted data from Haytham (+extension).xlsx")
timesteps = data["Time step"]
demand = data["Users consumption (kWh)"]

fig, ax = plt.subplots()

ax.plot(
    timesteps,
    demand,
    linewidth=2,
    marker="o",
    markeredgecolor="None",
    color=_color_demand,
)
ax.set_xlabel("Time", fontsize=12)
ax.set_ylabel("Electricity demand (in kWh)", fontsize=12)
ax.set_ylim([0, max(demand) * 1.15])
ax.set_xlim([-1, max(timesteps) + 1])

set_x_ticklabels_function(ax)

ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))
plt.tight_layout()
plt.show()
fig.savefig("electricity demand.pdf", dpi=1000)

#
#
#
#

price = data["Selling Price [$/kWh]"]
governmental = data["Governmental Pricing [$/kWh]"]
fig, ax = plt.subplots()
ax.plot(
    timesteps,
    price,
    linewidth=2,
    marker="o",
    markeredgecolor="None",
    color=_color_price,
)
ax.set_ylabel("Electricity price (in $/kWh)", fontsize=12)
ax.set_xlabel("Time", fontsize=12)
set_x_ticklabels_function(ax)
ax.set_ylim([0, max(price) * 1.15])
ax.set_xlim([-1, max(timesteps) + 1])
plt.tight_layout()
plt.show()
fig.savefig("electricity selling price.pdf", dpi=1000)

#
#
#
#
# LN(Price)

fig, ax = plt.subplots()
price_ln = np.log(price)
ax.plot(
    timesteps,
    price_ln,
    linewidth=2,
    marker="o",
    markeredgecolor="None",
    color=_color_price,
    linestyle="solid",
)
ax.set_ylabel("ln(Electricity price)", fontsize=12)
ax.set_xlabel("Time", fontsize=12)
set_x_ticklabels_function(ax)
ax.set_xlim([-1, max(timesteps) + 1])
plt.tight_layout()
plt.show()
fig.savefig("LN electricity selling price.pdf", dpi=1000)

# LN(Price)
fig, ax = plt.subplots()
demand_ln = np.log(demand)
ax.plot(
    timesteps,
    demand_ln,
    linewidth=2,
    marker="o",
    markeredgecolor="None",
    color=_color_demand,
)
ax.set_ylabel("ln(Electricity demand)", fontsize=12)
ax.set_xlabel("Time", fontsize=12)
set_x_ticklabels_function(ax)
ax.set_xlim([-1, max(timesteps) + 1])
plt.tight_layout()
plt.show()
fig.savefig("LN electricity demand.pdf", dpi=1000)

# ACF(Demand)
fig, _ax = plt.subplots()
plot_acf(
    ax=_ax,
    x=demand,
    color=_color_demand,
    vlines_kwargs={"colors": _color_demand},
    mec=_color_demand,
)

_ax.set_ylim([-1.1, 1.1])
for item in _ax.collections:
    if type(item) == PolyCollection:
        item.set_facecolor("#C39898")
        item.set_edgecolor("none")
        item.set_linewidth(1.5)

_ax.set_title("")

plt.tight_layout()

plt.show()
fig.savefig("ACF electricity demand.pdf", dpi=1000)


# ACF(Price)
fig, _ax = plt.subplots()
plot_acf(
    ax=_ax,
    x=price,
    color=_color_price,
    vlines_kwargs={"colors": _color_price},
    mec=_color_price,
)
_ax.set_ylim([-1.1, 1.1])

for item in _ax.collections:
    if type(item) == PolyCollection:
        item.set_facecolor("#6C946F")
        item.set_edgecolor("none")
        item.set_linewidth(1.5)
_ax.set_title("")
plt.tight_layout()
plt.show()
fig.savefig("ACF electricity price.pdf", dpi=1000)
