####################
# Packages used by modules
####################
# import pandas as pd
# import sqlite3
# import math
# import numpy as np
# import sys
# import os

####################
# Import Functions
####################

import nasem_dairy as nd

# # Reload the module
# import importlib
# nd = importlib.reload(nd)


###############################

# animal_input is a dictionary with all animal specific parameters
# diet_info is a dataframe with the user entered feed ingredients and %DM intakes
diet_info, animal_input, equation_selection = nd.read_input('src/nasem_dairy/data/input.txt')


# Execute function

# Assign values here so they can be see in environment
# coeff_dict is imported from ration_balancer, see coeff_dict.py
NASEM_out = nd.NASEM_model(diet_info, animal_input, equation_selection, 'src/nasem_dairy/data/diet_database.db', nd.coeff_dict)

import pandas as pd
# Display results, temporary
def display_diet_values(df):
    components = ['Fd_CP', 'Fd_RUP_base', 'Fd_NDF', 'Fd_ADF', 'Fd_St', 'Fd_CFat', 'Fd_Ash']
    rows = []

    for component in components:
        percent_diet = round(df.loc['Diet', component + '_%_diet']) #.values[0], 2)
        kg_diet = round(df.loc['Diet', component + '_kg/d'])    #.values[0], 2)
        rows.append([component, percent_diet, kg_diet])

    headers = ['Component', '% DM', 'kg/d']

    table = pd.DataFrame(rows, columns = headers)

    return table



model_data = pd.DataFrame(NASEM_out["model_results"], index=['Value']).T


diet_data  = display_diet_values(NASEM_out["diet_info"])

print(model_data)
print(diet_data)
