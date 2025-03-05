import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# import scienceplots
import matplotlib as mpl
from statsmodels.graphics.tsaplots import plot_acf
from matplotlib.collections import PolyCollection
import matplotlib.ticker as ticker

"""
    DEFINE COLORS AND PARAMETERS
"""

_color_demand = "#024CAA"
_color_price = "#EB8317"

_factor = 2.2
_fontsize=14

plt.style.use("classic")
plt.rcParams["figure.figsize"] = [8, 4]
plt.rcParams["xtick.labelsize"] = _fontsize
plt.rcParams["ytick.labelsize"] = _fontsize


def mark_highest_value_per_year(ax, values):
    num_years = len(values) // 12
    for y in range(num_years):
        max_value = values.iloc[y*12:y*12+12].max()
        max_index = values.iloc[y*12:y*12+12][values.iloc[y*12:y*12+12] == max_value].index[0]  # First occurrence
        ax.text(max_index, max_value + 19500,  
                f"{max_value:,.0f}", ha='center', fontsize=_fontsize, color=_color_demand,
                bbox=dict(facecolor='none', edgecolor=_color_demand, boxstyle='round')
                )
    return


def mark_lowest_value_per_year(ax, values):
    num_years = len(values) // 12
    for y in range(num_years):
        min_value = values.iloc[y*12:y*12+12].min()
        min_index = values.iloc[y*12:y*12+12][values.iloc[y*12:y*12+12] == min_value].index[0]  # First occurrence
        if min_index == 2:
            _x_offset = 0
            _y_offset = 0.06
        else:
            _x_offset = 2.2
            _y_offset = -0.06
        ax.text(min_index + _x_offset, min_value + _y_offset,  
                f"{min_value:,.2f}", ha='center', fontsize=_fontsize, color=_color_price,
                bbox=dict(facecolor='none', edgecolor=_color_price, boxstyle='round')
                )
    return


def set_x_ticklabels_function(axis):
    x_points = [0, 6, 12, 18, 24, 30, 36]
    axis.set_xticks(x_points)
    axis.set_xticklabels(
        ["01|2021", "07|2021", "01|2022", "07|2022", "01|2023", "07|2023", "01|2024"]
    )
    for point in x_points[::2]:
        axis.axvline(point, linestyle="--", color="gray", zorder=0)
    return


"""
    GET DATA
"""

data = pd.read_excel("../model/1_sorted data from Haytham (+extension).xlsx")
timesteps = data["Time step"]
demand = data["Users consumption (kWh)"]


"""
    USERS CONSUMPTION (in kWh)
"""

fig, ax = plt.subplots(figsize=(_factor * 3.25, _factor * 1.25))

ax.plot(
    timesteps,
    demand,
    linewidth=2,
    marker="o",
    markeredgecolor="None",
    color=_color_demand,
)
# ax.set_xlabel("Time", fontsize=_fontsize)
ax.set_ylabel("Consumption (in kWh)", fontsize=_fontsize)
ax.set_ylim([0, max(demand) * 1.15])
ax.set_xlim([-1, max(timesteps) + 1])

x_points = [0, 6, 12, 18, 24, 30, 36]
ax.set_xticks(x_points)
ax.set_xticklabels(
    ["01|2021", "07|2021", "01|2022", "07|2022", "01|2023", "07|2023", "01|2024"],
    rotation=15
)
for point in x_points[::2]:
    ax.axvline(point, linestyle="--", color="gray", zorder=0)
    
ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1, lw=0.5)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

# mark_highest_value_per_year(ax, demand)
# ax.set_ylim([0, 445000])
ax.set_yticks([0, 100000, 200000, 300000, 400000])
plt.tight_layout()
plt.show()
fig.savefig("observation_electricity demand.pdf", dpi=1000)


"""
    SELLING PRICE (in $/kWh)
"""

price = data["Selling Price [$/kWh]"]
governmental = data["Governmental Pricing [$/kWh]"]
fig, ax = plt.subplots(figsize=(_factor * 3.25, _factor * 1.25))
ax.plot(
    timesteps,
    price,
    linewidth=2,
    marker="o",
    markeredgecolor="None",
    color=_color_price,
)
ax.set_ylabel("Selling price (in $/kWh)", fontsize=_fontsize)
ax.set_xticks(x_points)
ax.set_xticklabels(
    ["01|2021", "07|2021", "01|2022", "07|2022", "01|2023", "07|2023", "01|2024"],
    rotation=15
)
for point in x_points[::2]:
    ax.axvline(point, linestyle="--", color="gray", zorder=0)
ax.set_ylim([0, max(price) * 1.15])
ax.set_xlim([-1, max(timesteps) + 1])
ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1, lw=0.5)
# mark_lowest_value_per_year(ax, price)
plt.tight_layout()
plt.show()
fig.savefig("observation_electricity selling price.pdf", dpi=1000)

"""
    LN of SELLING PRICE (in $/kWh)
"""

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
fig.savefig("LN_electricity selling price.pdf", dpi=1000)

"""
    LN of ELECTRICITY DEMAND (in kWh)
"""

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
fig.savefig("LN_electricity demand.pdf", dpi=1000)


"""
    ACF of ELECTRICITY DEMAND (in kWh)
"""

fig, _ax = plt.subplots(figsize=(_factor * 2, _factor * 2))

plot_acf(
    ax=_ax,
    x=demand[6:],
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
fig.savefig("ACF_electricity demand.pdf", dpi=1000)









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
fig.savefig("ACF_electricity price.pdf", dpi=1000)









iteration = [
    ["Governmental Pricing [$/kWh]", "governmental pricing"],
    ["Average hours of sun", "average sun hours"],
    ["Average temperature (high) [°C]", "average temperature (high)"],
    ["Average temperature (low) [°C]", "average temperature (low)"],
    ["Availability of the public grid [hours]", "public grid availability"],
    ["Rooftop solar PV systems [kW]", "rooftop pv"],
    ["Solar farms [kW]", "farm pv"]
    ]

for _item, _name in iteration:
    _observation = data[_item]
    
    fig, ax = plt.subplots()
    ax.plot(
        timesteps,
        _observation,
        linewidth=2,
        marker="o",
        markeredgecolor="None",
        color="black"
    )
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel(_item, fontsize=12)
    ax.set_ylim([0, max(_observation) * 1.15])
    ax.set_xlim([-1, max(timesteps) + 1])

    set_x_ticklabels_function(ax)

    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))
    plt.tight_layout()
    plt.show()
    fig.savefig("observation_"+_name+".pdf", dpi=1000)
    
    # LN(Price)
    fig, ax = plt.subplots()
    observation_ln = np.log(_observation)
    ax.plot(
        timesteps,
        observation_ln,
        linewidth=2,
        marker="o",
        markeredgecolor="None",
        color='black',
    )
    ax.set_ylabel("ln("+_item+")", fontsize=12)
    ax.set_xlabel("Time", fontsize=12)
    set_x_ticklabels_function(ax)
    ax.set_xlim([-1, max(timesteps) + 1])
    plt.tight_layout()
    plt.show()
    fig.savefig("LN_"+_name+".pdf", dpi=1000)
    
    fig, _ax = plt.subplots()
    plot_acf(
        ax=_ax,
        x=_observation,
        color='black',
        vlines_kwargs={"colors": "black"},
        mec="gray",
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
    fig.savefig("ACF_"+_name+".pdf", dpi=1000)
    









