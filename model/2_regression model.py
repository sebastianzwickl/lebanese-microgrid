import pandas as pd
import numpy as np
import statsmodels.api as sm
import utils as u

"FETCH AND CHECK INPUT DATA"
input_data = pd.read_excel('1_sorted data from Haytham (+extension).xlsx')
_columns = u.check_columns_with_nan_values(input_data)

print('NOTE: The following columns are removed because they contain nan entries:')
if len(_columns) != 0:
    for _i in _columns:
        print('- '+_i)

input_data_clean = input_data.drop(_columns, axis=1)
print('')
_relevant_columns = ['Selling Price [$/kWh]', 
                    # 'Governmental Pricing [$/kWh]', 
                     'Average hours of sun',
                    'Average temperature (high) [°C]',
#                    'Average temperature (low) [°C]',
#                     'Availability of the public grid [hours]',
                     'Rooftop solar PV systems [kW]',
                    'Solar farms [kW]'
                     ]

for _c in _relevant_columns:
    input_data_clean['LN_'+_c] = np.log(input_data_clean[_c])
    
# log log direkt als elastizität bestimmen kann...
#kd produktion => exponent direkt faktor

"PREPARE MODEL"

_updated = []
for el in _relevant_columns:
    _updated.append('LN_'+el)
    
X = input_data_clean.filter(items=_updated)

X = sm.add_constant(X)

y = np.log(input_data_clean['Users consumption (kWh)'])

model = sm.OLS(y, X).fit()
print(model.summary())
electricity_demand_elasticity = model.params['LN_Selling Price [$/kWh]']
print('')
print("+ ESTIMATED ELECTRICITY DEMAND ELASTICITY: {:.4f}".format(electricity_demand_elasticity))

print(model.params)