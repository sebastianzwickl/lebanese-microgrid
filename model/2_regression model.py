import pandas as pd
import numpy as np
import statsmodels.api as sm
import utils as u

_DATA_SOURCE = '2_sorted data from Haytham (updated Nov 24).xlsx'

"""
    FETCH AND CHECK INPUT DATA
"""
input_data = pd.read_excel(_DATA_SOURCE).loc[5:]
_columns = u.check_columns_with_nan_values(input_data)

print('NOTE: The following columns are removed because they contain nan entries:')
if len(_columns) != 0:
    for _i in _columns:
        print('- '+_i)
print('')
 
       
"""
    PREPARE INPUT DATA
    Also ich würde Equ 1 zuerst mit allen Parametern schätzen und dann 
    noch einmal nur mit jenen,  die bei der ersten Schätzung signifikant waren 
    (t> 1.96 oder  p< 0.05)

"""

input_data_clean = input_data.drop(_columns, axis=1)
_regressors = [
    'Selling Price [$/kWh]', # (\alpha_1; P_t)
    'Average hours of sun', # (\alpha_2; S_t)
    'HDD', # (\alpha_3; HDD)
    'CDD', # (\alpha_4; CDD)
    'Public Grid Time [%]', # (\alpha_5; PG_t)
    'Rooftop solar PV systems [kW]', # (\alpha_6; RPV_t)
    'Solar farms [kW]', # (\alpha_7; FPV_t)
                      ]

for _c in _regressors:
    li = list(input_data_clean[_c])
    if 0 in li:
        new_list = [1 if el==0 else el for el in li]
        input_data_clean[_c] = new_list
    else:
        pass
    
    input_data_clean['LN_'+_c] = np.log(input_data_clean[_c])

_updated = []
for el in _regressors:
    _updated.append('LN_'+el)

"""
    PREPARE INPUT DATA
"""

X = input_data_clean.filter(items=_updated)
X = sm.add_constant(X)
y = np.log(input_data_clean['Users consumption (kWh)'])

model = sm.OLS(y, X).fit()
print(model.summary())
electricity_demand_elasticity = model.params['LN_Selling Price [$/kWh]']
print('')
print("+ ESTIMATED ELECTRICITY DEMAND ELASTICITY: {:.4f}".format(electricity_demand_elasticity))
print('')
print(model.params)