import statsmodels.formula.api as smf




def model(
    dependent_variable,
    control_list,
    dataframe,
    no_trend: bool,
    fitting_end,
    fitting_start,
):
    if no_trend:
        if dataframe is dfx:
            m = f"{dependent_variable} ~ 1 + C(month) + C(weekday) + " + " + ".join(
                control_list
            )
        else:
            m = f"{dependent_variable} ~ 1 + C(month) +" + " + ".join(control_list)
    else:
        if dataframe is dfx:
            m = (
                f"{dependent_variable} ~ 1 + time + C(month) + C(weekday) + "
                + " + ".join(control_list)
            )
        else:
            m = f"{dependent_variable} ~ 1 + time + C(month) + " + " + ".join(
                control_list
            )

    return smf.ols(
        m,
        dataframe[
            (dataframe.index >= fitting_start) & (dataframe.index <= fitting_end)
        ],
    ).fit(cov_type="HAC", cov_kwds={"maxlags": 7})


import statsmodels.formula.api as smf




def model(
    dependent_variable,
    control_list,
    dataframe,
    no_trend: bool,
    fitting_end,
    fitting_start,
):
    if no_trend:
        if dataframe is dfx:
            m = f"{dependent_variable} ~ 1 + C(month) + C(weekday) + " + " + ".join(
                control_list
            )
        else:
            m = f"{dependent_variable} ~ 1 + C(month) +" + " + ".join(control_list)
    else:
        if dataframe is dfx:
            m = (
                f"{dependent_variable} ~ 1 + time + C(month) + C(weekday) + "
                + " + ".join(control_list)
            )
        else:
            m = f"{dependent_variable} ~ 1 + time + C(month) + " + " + ".join(
                control_list
            )

    return smf.ols(
        m,
        dataframe[
            (dataframe.index >= fitting_start) & (dataframe.index <= fitting_end)
        ],
    ).fit(cov_type="HAC", cov_kwds={"maxlags": 7})