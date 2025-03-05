import numpy as np
import pyomo.environ as py
from datetime import datetime
import pandas as pd
import os

_now = datetime.now().strftime("%Y%m%d_%H%M")
result_dir = os.path.join("result", "{}".format(_now))
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

_list_profit_final = []
_list_suppressed_final = []
_list_elasticity_final = []
_list_price_final = []

# for _ELASTICITY in list(range(0, -101, -1)):
# for _ELASTICITY in list(range(0, -2, -1)):
for _ELASTICITY in [-47.88]:
    _ELASTICITY = 1 * _ELASTICITY / 100
    print('Elasticity: {}'.format(_ELASTICITY))
    # _ELASTICITY = -0.4788 # (in $/kWh)
    _REFERENCE_PRICE = 0.3053
    _REFERENCE_DEMAND = 141566
    
    _dict_profit = []
    _dict_obj = []
    _dict_met = []
    _dict_sup = []
    _dict_price_delta = []
    _dict_ref_price = []
    _dict_new_price = []
    _dict_delta_profit = []
    _share_suppressed_demand = []
    _relative_increase_price = []
    
    for _YEAR in [2021, 2022, 2023, 2024]:
        for _MONTH in list(range(1, 13, 1)):
            if (_YEAR == 2024) and (_MONTH == 6):
                break
            else:
                pass
    
            model = py.ConcreteModel()
    
            model.var_q_met = py.Var(within=py.NonNegativeReals, doc="VAR: q^{met}")
    
            model.var_q_suppressed = py.Var(doc="VAR: q^{suppressed}")
    
            model.var_delta_p = py.Var(doc="VAR: \Delta{p}")
    
            model.var_lambda1 = py.Var(doc="VAR: lambda_{1}")
            model.var_lambda2 = py.Var(doc="VAR: lambda_{2}")
            model.var_mhu1 = py.Var(within=py.NonNegativeReals, doc="VAR: mhu_{1}")
            model.var_mhu2 = py.Var(within=py.NonNegativeReals, doc="VAR: mhu_{2}")
    
            Data = pd.read_excel("2_sorted data from Haytham (updated Nov 24).xlsx")
            
            price = Data.loc[:, ["Year", "Month", "Time step", "Selling Price [$/kWh]"]]
            _value = price.loc[(price.Year == _YEAR) & (price.Month == _MONTH)][
                "Selling Price [$/kWh]"
            ].item() 
            model.par_price_ref = py.Param(initialize=_value)
            
            demand = Data.loc[:, ["Year", "Month", "Time step", "Users consumption (kWh)"]]
            _value = demand.loc[(demand.Year == _YEAR) & (demand.Month == _MONTH)][
                "Users consumption (kWh)"
            ].item()
            # _value = 80213 * _value**(_ELASTICITY)
            model.par_demand = py.Param(initialize=_value)
    
            model.par_elasticity = py.Param(initialize=_ELASTICITY)
    
            model.binary1 = py.Var(within=py.Binary)
            model.binary2 = py.Var(within=py.Binary)
    
            def constraint_1(model):
                return model.var_lambda1 - model.var_mhu1 + model.var_mhu2 == 0
    
            model.constraint_1 = py.Constraint(rule=constraint_1, doc='Implemented!')
    
            def constraint_2(model):
                return -model.var_lambda1 + model.var_lambda2 == 0
    
            model.constraint_2 = py.Constraint(rule=constraint_2, doc='Implemented!')
    
            def constraint_3(model):
                return model.var_q_met - model.var_q_suppressed - model.par_demand == 0
    
            model.constraint_3 = py.Constraint(rule=constraint_3, doc='Implemented!')
    
            def constraint_4(model):
                return (
                    model.var_q_suppressed
                    - model.var_delta_p
                    / model.par_price_ref
                    * model.par_elasticity
                    * model.par_demand
                    == 0
                )
    
            model.constraint_4 = py.Constraint(rule=constraint_4, doc='Implemented!')
    
            def constraint_51(model):
                return model.var_mhu1 <= 10e8 * model.binary1
    
            model.constraint_51 = py.Constraint(rule=constraint_51, doc='Implemented!')
    
            def constraint_52(model):
                return model.var_q_met <= 10e8 * (1 - model.binary1)
    
            model.constraint_52 = py.Constraint(rule=constraint_52, doc='Implemented!')
    
            def constraint_61(model):
                return model.var_mhu2 <= 10e8 * model.binary2
    
            model.constraint_61 = py.Constraint(rule=constraint_61, doc='Implemented!')
    
            def constraint_62(model):
                return -model.var_q_met + 1.0 * model.par_demand <= 10e8 * (
                    1 - model.binary2
                )
    
            model.constraint_62 = py.Constraint(rule=constraint_62, doc='Implemented!')
    
            model.set_n = py.Set(initialize=range(0, 200, 1), doc='Implemented!')
            model.var_z = py.Var(model.set_n, within=py.NonNegativeReals, doc='Implemented!')
            model.var_sigma = py.Var(model.set_n, within=py.Binary, doc='Implemented!')
    
            def constraint_71(model, step):
                return model.var_z[step] <= 10e8 * model.var_sigma[step]
    
            model.constraint_71 = py.Constraint(model.set_n, rule=constraint_71, doc='Implemented!')
    
            def constraint_72(model, step):
                return model.var_z[step] <= model.var_q_met
    
            model.constraint_72 = py.Constraint(model.set_n, rule=constraint_72, doc='Implemented!')
    
            def constraint_73(model, step):
                return (
                    model.var_q_met - (1 - model.var_sigma[step]) * 10e8
                    <= model.var_z[step]
                )
    
            model.constraint_73 = py.Constraint(model.set_n, rule=constraint_73, doc='Implemented!')
    
            def constraint_8(model):
                return model.var_delta_p == sum(
                    model.var_sigma[step] * model.par_price_ref / 200 for step in model.set_n
                )
    
            model.constraint_8 = py.Constraint(rule=constraint_8)
    
            def objective(model):
                return model.var_q_met * model.par_price_ref + sum(
                    model.par_price_ref / 100 * model.var_z[step] for step in model.set_n
                )
    
            model.objective = py.Objective(expr=objective, sense=py.maximize)
    
            solver = py.SolverFactory("gurobi")
            solution = solver.solve(model)
    
            _val = model.par_price_ref() * model.par_demand()
            _dict_profit.append(_val)
            _dict_obj.append(model.objective())
            _dict_delta_profit.append((model.objective() - _val)/_val)
            _dict_met.append(model.var_q_met())
            _dict_sup.append(model.var_q_suppressed())
            _dict_price_delta.append(model.var_delta_p())
            _dict_ref_price.append(model.par_price_ref())
            _val = model.par_price_ref() + model.var_delta_p()
            _dict_new_price.append(_val)
            _share_suppressed_demand.append(model.var_q_suppressed() / (-model.var_q_suppressed() + model.var_q_met())) 
            _relative_increase_price.append(model.var_delta_p()/model.par_price_ref())
    _dict = {
        "Profit (from data)": _dict_profit,
        "Profit (from model)": _dict_obj,
        "Delta profit (model - data) (in %)": _dict_delta_profit,
        "Met demand (in kWh)": _dict_met,
        "Suppressed demand (in kWh)": _dict_sup,
        "Reference price (in $/kWh)": _dict_ref_price,
        "Modeled price (in $/kWh)": _dict_new_price, 
        "Share of suppressed demand (in %)": _share_suppressed_demand,
        "Relative price increase (in %)": _relative_increase_price
    }
    df = pd.DataFrame(_dict)
    df.to_excel(os.path.join(result_dir, "_RESULTS_timeseries.xlsx"), index=False)
    
    # _list_delta_price = []
    # _list_delta_price_percent = []
    # for i in range(0, len(_dict_ref_price)-1, 1):
    #     _val = _dict_ref_price[i+1] - _dict_new_price[i]
    #     _list_delta_price.append(np.around(_val, 5))
    #     _list_delta_price_percent.append(_val/_dict_ref_price[i+1])
        
    # _dict = {
    #     "Delta in price (in $/kWh)": _list_delta_price,
    #     "Delta (in %)": _list_delta_price_percent
    # }
    # df = pd.DataFrame(_dict)
    # df.to_excel("_RESULTS_delta.xlsx", index=False)    
    _p = np.around(np.mean(_dict_delta_profit)*100, 2)
    print("Increase in profit: {}".format(_p))
    _s = np.around(np.mean(_share_suppressed_demand) * 100, 2)
    print("Share of suppressed demand: {}".format(_s))
    # _dict_profit_final[_ELASTICITY] = _p
    # _dict_suppressed_final[_ELASTICITY] = _s
    
    _list_profit_final.append(_p)
    _list_suppressed_final.append(_s)
    _list_elasticity_final.append(_ELASTICITY)
    _list_price_final.append(np.mean(_relative_increase_price)*100)

if _ELASTICITY != -0.4788:
    _dict = {
        "Elasticity": _list_elasticity_final,
        "Profit increase (in %)": _list_profit_final,
        "Price increase (in %)": _list_price_final,
        "Suppressed demand (in %)": _list_suppressed_final,
    }
    df = pd.DataFrame(_dict)
    df.to_excel(os.path.join(result_dir, "_RESULTS_sensitivity.xlsx"), index=False)  
    
