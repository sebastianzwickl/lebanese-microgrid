import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import scienceplots

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
Data = pd.read_excel("result/" + _time + "/_RESULTS_timeseries.xlsx")
Data["Cumulative Profit (from data)"] = Data["Profit (from data)"].cumsum()
Data["Cumulative Profit (from model)"] = Data["Profit (from model)"].cumsum()


fig, ax = plt.subplots(figsize=(_factor * 4.5, _factor * 1.5))

ax.plot(
    list(range(0, len(Data["Cumulative Profit (from data)"]), 1)),
    Data["Cumulative Profit (from data)"],
    linewidth=2,
    # marker="o",
    markeredgecolor="None",
    color=_color_line1,
    label="Data",
    zorder=3,
)

ax.plot(
    list(range(0, len(Data["Cumulative Profit (from model)"]), 1)),
    Data["Cumulative Profit (from model)"],
    linewidth=2,
    # marker="o",
    markeredgecolor="None",
    color=_color_line2,
    label="Model",
)
x = list(range(0, len(Data["Cumulative Profit (from data)"]), 1))
y1 = Data["Cumulative Profit (from data)"]
y2 = Data["Cumulative Profit (from model)"]

_change = (sum(y2) - sum(y1)) / sum(y1) * 100
_change = np.around(_change, 1)


ax.fill_between(x, y1, y2, color=_color_area, label=r"+" + str(_change) + r"\%")


ax.set_ylabel(r"Cumulative revenues (in \$)", fontsize=_fontsize)
# ax.set_ylim([0, max(y2) * 1.125])
# ax.set_xlim([-1, max(timesteps) + 1])

set_x_ticklabels_function(ax)
ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1, lw=0.5)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

_legend = ax.legend(
    loc="upper left",
    facecolor="white",
    fontsize=14,
    handlelength=1.5,
    handletextpad=0.5,
    ncol=3,
    borderpad=0.35,
    columnspacing=0.75,
    edgecolor="black",
    frameon=True,
    bbox_to_anchor=(0, 1),
    shadow=False,
    framealpha=1,
)

plt.tight_layout()
plt.show()
fig.savefig("result/" + _time + "/RESULTS_comparison_of_profits.pdf", dpi=1000)

###############################################################################

fig, ax = plt.subplots(figsize=(_factor * 4.5*0.65, _factor * 1.5*0.65))
_str = str(np.around((1 + Data["Share of suppressed demand (in %)"][0]) * 100, 1))

_x_values = list(range(0, len(Data["Cumulative Profit (from data)"]), 1))
_x_values = [x-1.1 for x in _x_values]

ax.bar(
    _x_values,
    Data["Met demand (in kWh)"],
    color="#72BAA9",
    label=r"Supplied ({}\%)".format(_str),
    zorder=2,
)

_values = Data["Suppressed demand (in kWh)"].values * (-1)
_bottom = Data["Met demand (in kWh)"]

_str = str(np.around(Data["Share of suppressed demand (in %)"][0] * -100, 1))

ax.bar(
    _x_values,
    _values,
    bottom=_bottom,
    color="#D8C4B6",
    label=r"Suppressed ({}\%)".format(_str),
    zorder=2,
)

set_x_ticklabels_function(ax)
# ax.set_xlim([-1.75, 41])
ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1, lw=0.5)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

ax.set_ylabel(r"Demand (in kWh)", fontsize=_fontsize)

_legend = ax.legend(
    loc="upper right",
    facecolor="white",
    fontsize=14,
    handlelength=1.5,
    handletextpad=0.5,
    ncol=3,
    borderpad=0.35,
    columnspacing=0.75,
    edgecolor="black",
    frameon=True,
    bbox_to_anchor=(1, 1),
    shadow=False,
    framealpha=1,
)

plt.tight_layout()
fig.savefig("result/" + _time + "/RESULTS_demand_met_suppressed.pdf", dpi=1000)

###############################################################################

fig, ax = plt.subplots(figsize=(_factor * 4.5*0.65, _factor * 1.5*0.65))

_values = []
for index, row in Data.iterrows():
    _values.append(row["Modeled price (in $/kWh)"] - row["Reference price (in $/kWh)"])

ax.bar(
    _x_values,
    _values,
    color="#9AA6B2",
    zorder=3,
)

ax.set_ylabel(r"Increase (in \$/kWh)", fontsize=_fontsize)

x_points = [0, 6, 12, 18, 24, 30, 36]
ax.set_xticks(x_points)
ax.set_xticklabels(
    ["01-2021", "07-2021", "01-2022", "07-2022", "01-2023", "07-2023", "01-2024"],
    fontsize=13
)

ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1, lw=0.5)


def yday2date(x):
    return x * 240 * 10 / 6


def back(y):
    return y / 240 * 10 / 6


secax_y = ax.secondary_yaxis(-0.145, functions=(yday2date, back))

secax_y.set_ylabel(r"Rel. increase (in \%)", fontsize=_fontsize, color="#A64D79")
secax_y.tick_params(axis="y", colors="#A64D79")
secax_y.spines["left"].set_color("#A64D79")
secax_y.tick_params(axis="y", colors="#A64D79", which="both")
ax.plot(
    _x_values,
    len(Data["Cumulative Profit (from data)"]) * [0.25 * 54 / 100],
    color="#A64D79",
    lw=2.5,
    zorder=3,
    ls="dashed",
)

plt.tight_layout()
plt.show()
fig.savefig("result/" + _time + "/RESULTS_comparison_of_prices.pdf", dpi=1000)

###############################################################################

fig, ax = plt.subplots(figsize=(_factor * 4.5 * 0.65, _factor * 1.5 * 0.65))

data = pd.read_excel("_RESULTS_sensitivity.xlsx")

_x = data["Elasticity"] * (-1)
_y = data["Profit increase (in %)"]
ax.plot(_x, _y, label="Relative revenue increase", lw=2, ls="solid", color='#3A7D44')
ax.plot(
    _x,
    data["Price increase (in %)"],
    label="Relative price increase",
    lw=2,
    ls="dashed",
    color="#A64D79",
)
ax.plot(
    _x,
    data["Suppressed demand (in %)"] * (-1),
    label="Suppressed demand share",
    lw=2,
    ls="solid",
    color="#D8C4B6",
)
ax.set_xlim([0.2, 0.8])
# ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{-x:.2f}"))
ax.set_ylabel(r"Sensitivity (in \%)", fontsize=_fontsize)

# set_x_ticklabels_function(ax)
ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1, lw=0.5)
# ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

_legend = ax.legend(
    loc="upper right",
    facecolor="white",
    fontsize=14,
    handlelength=1.5,
    handletextpad=0.5,
    ncol=1,
    borderpad=0.35,
    columnspacing=0.75,
    edgecolor="black",
    frameon=True,
    bbox_to_anchor=(1, 1),
    shadow=False,
    framealpha=1,
)

for point in [0.4788]:
    ax.axvline(point, linestyle="solid", color="black", zorder=1)

ax.set_xlabel('Selling price elasticity (-)', fontsize=_fontsize)

ax.axvspan(0.36, 0.58, color='#A6AEBF', alpha=0.25, zorder=0)

plt.tight_layout()
fig.savefig("result/" + _time + "/RESULTS_change_by_elasticity.pdf", dpi=1000)

###############################################################################

fig, ax = plt.subplots(figsize=(_factor * 3.5, _factor * 1.5))

_mexico_year = [2002, 2012]
_mexico_value = [0.36]

_iran_year = [2001, 2008]
_iran_value = [0.02]

_chile_year = [2006]
_chile_value = [0.40]

_mozambik_year = [2002, 2003]
_mozambik_value = [0.49]
_mozambik_value2 = [0.66]

_brazil_year2 = [2008, 2013]
_brazil_value = [0.5]

_years = list(range(2000, 2026, 1))

ax.plot(
    _mexico_year,
    2 * _mexico_value,
    marker="o",
    color="#FFCF50",
    lw=1.5,
    ls="solid",
    label=r"Mexico (-" + str(_mexico_value[0]) + ")",
)
ax.plot(
    _iran_year,
    2 * _iran_value,
    marker="o",
    color="#5C7285",
    lw=1.5,
    ls="solid",
    label="Iran (-" + str(_iran_value[0]) + ")",
)
ax.plot(
    _chile_year,
    1 * _chile_value,
    marker="o",
    lw=1.5,
    ls="solid",
    label="Chile (-" + str(_chile_value[0]) + ")",
    color="#98D8EF",
)
ax.plot(
    _mozambik_year,
    2 * [0.58],
    marker="o",
    color="#B9B28A",
    lw=1.5,
    ls="solid",
    label="Mozambik (-"+str(0.58)+')'
)
# ax.plot(
#     _mozambik_year,
#     2 * _mozambik_value2,
#     marker="o",
#     color="#B9B28A",
#     lw=1.5,
#     ls="solid",
# )
ax.plot(
    _brazil_year2,
    2 * _brazil_value,
    marker="o",
    color="#E195AB",
    lw=1.5,
    ls="solid",
    label="Brazil (-"+str(_brazil_value[0])+')'
)

ax.plot(
    [2021, 2024],
    [0.4788, 0.4788],
    marker="o",
    color="black",
    lw=1.5,
    ls="solid",
    label="Lebanon (-"+ str(0.48)+')'
)

ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1, lw=0.5)

_legend = ax.legend(
    loc="lower right",
    facecolor="white",
    fontsize=14,
    handlelength=1.5,
    handletextpad=0.5,
    ncol=2,
    borderpad=0.35,
    columnspacing=0.75,
    edgecolor="black",
    frameon=True,
    bbox_to_anchor=(1, 0),
    shadow=False,
    framealpha=1,
)

ax.set_ylabel(r"Selling price elasticity (-)", fontsize=_fontsize)
ax.set_xlabel(r"Year", fontsize=_fontsize)

plt.tight_layout()
fig.savefig("result/" + _time + "/RESULTS_elasticity_comparison.pdf", dpi=1000)

###############################################################################

fig, ax = plt.subplots(figsize=(_factor * 2.5, _factor * 1.5))
_value_0=sum(Data["Profit (from data)"])
ax.bar(1, sum(Data["Profit (from data)"]), color='#DF6D14', zorder=2)
ax.text(1, sum(Data["Profit (from model)"]) * 0.045 + _value_0, 
        s=r'({:,.0f})'.format(_value_0), 
        ha='center', va='center', fontsize=_fontsize)


ax.bar(2, sum(Data["Profit (from model)"]), color='#3A7D44', zorder=2)
_value = int(np.around(sum(Data["Profit (from model)"]), 0))
ax.text(2, sum(Data["Profit (from model)"]) * 1.045, 
        s=r'({:,.0f})'.format(_value), 
        ha='center', va='center', fontsize=_fontsize)


ax.set_ylabel(r"Revenues (in \$)", fontsize=_fontsize)
ax.plot([1.6, 2.4], 2*[_value_0], ls='dashed', color='white', lw=2)
_increase = np.around(((_value - _value_0)/_value_0)*100, 2)
ax.text(2, _value_0+(_value-_value_0)/2, s=r'+{}\%'.format(str(_increase)), va='center', ha='center', fontsize=_fontsize, color='white')

ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1, lw=0.5)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))


ax.set_ylim([0, 2000000])
ax.set_xlim([0.25, 2.75])
ax.set_xticks([1, 2])
ax.set_xticklabels(labels=['Data', 'Model'])
# _legend = ax.legend(
#     loc="upper left",
#     facecolor="white",
#     fontsize=14,
#     handlelength=1.5,
#     handletextpad=0.5,
#     ncol=3,
#     borderpad=0.35,
#     columnspacing=0.75,
#     edgecolor="black",
#     frameon=True,
#     bbox_to_anchor=(0, 1),
#     shadow=False,
#     framealpha=1,
# )

plt.tight_layout()
fig.savefig("result/" + _time + "/RESULTS_comparison_of_profits_barplot.pdf", dpi=1000)
