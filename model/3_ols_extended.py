import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import utils as u
import seaborn as sns
import matplotlib.pyplot as plt

import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)


_DATA_SOURCE = '2_sorted data from Haytham (updated Nov 24).xlsx'

"""
    FETCH AND CHECK INPUT DATA
"""
input_data = pd.read_excel(_DATA_SOURCE).loc[5:]
_columns = u.check_columns_with_nan_values(input_data)
print('**********************************************************************')
print('**********************************************************************')
print('NOTE: The following columns are removed because they contain NaN entries:')
if len(_columns) != 0:
    for _i in _columns:
        print('- ' + _i)
print('')
print('')
print('')

"""
    PREPARE INPUT DATA
"""
input_data_clean = input_data.drop(_columns, axis=1)
_regressors = [
    'Selling Price [$/kWh]', # (\alpha_1; P_t)
    #'Average hours of sun', # (\alpha_2; S_t)
    #'HDD', # (\alpha_3; HDD)
    #'CDD', # (\alpha_4; CDD)
    'Public Grid Time [%]', # (\alpha_5; PG_t)
    #'Rooftop solar PV systems [kW]', # (\alpha_6; RPV_t)
    #'Solar farms [kW]', # (\alpha_7; FPV_t)
    #'Weighed Rooftop solar PV systems [kW/kWh]',
    #'Weighed Rooftop solar PV systems (max) [kW/kWh]'
    'Solar PV penetration rate (in %)'
]

for _c in _regressors:
    li = list(input_data_clean[_c])
    if 0 in li:
        new_list = [1 if el == 0 else el for el in li]
        input_data_clean[_c] = new_list
    
    input_data_clean['LN_' + _c] = np.log(input_data_clean[_c])

_updated = ['LN_' + el for el in _regressors]


"""
    VIF TEST FOR MULTICOLLINEARITY
"""
X_vif = input_data_clean.filter(items=_updated)
X_vif = sm.add_constant(X_vif)

vif_data = pd.DataFrame()
vif_data["Variable"] = X_vif.columns
vif_data["VIF"] = [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
print('**********************************************************************')
print('**********************************************************************')
print("Variance Inflation Factor (VIF) Test Results:")
print(vif_data)
print('')
print('')
print('')

corr_matrix = input_data_clean[_updated].corr()
plt.figure(figsize=(16/2.5,9/2.5))
sns.heatmap(corr_matrix, annot=False, cmap="RdBu", fmt=".2f", linewidth=.5, mask=False, cbar=False)
for row in range(0, corr_matrix.shape[0], 1):
    for column in range(0, corr_matrix.shape[1], 1):
        _val = np.around(corr_matrix.values[row][column], 2)
        if (_val > 0.8) or (_val < -0.8):
            _color = 'white'
        else:
            _color = 'black'
        plt.text(column+0.5, row+0.5, str(_val), ha='center', va='center', color=_color, fontsize=12)
xticks = plt.gca().get_xticks()
xticklabels = plt.gca().get_xticklabels()
# xticklabels[0] = r'$ln(P_t)$'
# xticklabels[1] = '$ln(HDD_t)$'
# xticklabels[2] = '$ln(CDD_t)$'
# xticklabels[3] = '$ln(PG_t)$'
# xticklabels[4] = '$ln(SPV_t)$'
plt.gca().set_xticklabels(xticklabels, rotation=45)
xticks = plt.gca().get_xticks()
shift = -0.0  
plt.gca().set_xticks([x + shift for x in xticks])
plt.gca().set_xticklabels(xticklabels, rotation=45, fontsize=12)
plt.gca().xaxis.set_ticks_position('none') 
xticks = plt.gca().get_yticks()
xticklabels = plt.gca().get_yticklabels()
# xticklabels[0] = r'Selling price: $ln(P_t)$'
# xticklabels[1] = r'Heating degree day: $ln(HDD_t)$'
# xticklabels[2] = 'Cooling degree day: $ln(CDD_t)$'
# xticklabels[3] = 'Public grid time: $ln(PG_t)$'
# xticklabels[4] = 'Solar PV additions: $ln(SPV_t)$'
plt.gca().set_yticklabels(xticklabels, rotation=0, fontsize=12)
plt.tight_layout()  # Automatically adjust to prevent clipping
print('**********************************************************************')
print('**********************************************************************')
print("Create Correlation_plot.pdf")
print('')
print('')
print('')
plt.savefig('Correlation_plot_mod.pdf', dpi=1000)



"""
    REGRESSION MODEL
"""
X = input_data_clean.filter(items=_updated)
X = sm.add_constant(X)
y = np.log(input_data_clean['Users consumption (kWh)'])

model = sm.OLS(y, X).fit()
print('**********************************************************************')
print('**********************************************************************')
print(model.summary())

# Schätze die Preiselastizität
electricity_demand_elasticity = model.params['LN_Selling Price [$/kWh]']
print("\n+ ESTIMATED ELECTRICITY DEMAND ELASTICITY: {:.4f}".format(electricity_demand_elasticity))

