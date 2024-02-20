# Micronutrient Requirement Equations
import math

### CALCIUM ###
def calculate_Ca_Mlk(An_Breed: str) -> float:
    """
    Ca_Mlk: Calcium content of milk, g/L
    """
    if( An_Breed == "Jersey") | (An_Breed != ""):   
    # NOTE This makes no sense as if An_Breed is any string it gets assigned 1.17
    # So why check if it's a Jersey? No cow could be assigened 1.03 unless there is no An_Breed, 
    # but that would break the rest of the model
        Ca_Mlk = 1.17   # Calcium content of milk, g/L, Line 2963
    else:
        Ca_Mlk = 1.03
    return Ca_Mlk


def calculate_Fe_Ca_m(An_DMIn: float) -> float:
    """
    Fe_Ca_m: Ca requirement for maintenance, g/d
    """
    Fe_Ca_m = 0.9 * An_DMIn # maintenance, Line 2964
    return Fe_Ca_m


def calculate_An_Ca_g(An_BW_mature: float, An_BW: float, Body_Gain: float) -> float:
    """
    An_Ca_g: Ca requirement for growth, g/d
    """
    An_Ca_g = (9.83 * An_BW_mature**0.22 * An_BW**-.22) * Body_Gain     # Growth, Line 2965
    return An_Ca_g


def calculate_An_Ca_y(An_GestDay: int, An_BW: float) -> float:
    """
    An_Ca_y: Ca requirement for gestation, g/d
    """
    An_Ca_y = (0.0245 * math.exp((0.05581 - 0.00007 * An_GestDay) * An_GestDay) \
              - 0.0245 * math.exp((0.05581 - 0.00007 * (An_GestDay - 1)) * (An_GestDay - 1))) * An_BW / 715    # Gestation, Line 2966-2967 
    return An_Ca_y


def calculate_An_Ca_l(Mlk_NP_g: float, Ca_Mlk: float, Trg_MilkProd: float, Trg_MilkTPp: float) -> float:
    """
    An_Ca_l: Ca requirement for lactation, g/d
    """
    if Mlk_NP_g is None or math.isnan(Mlk_NP_g):    # Lactation, Line 2968
        An_Ca_l = Ca_Mlk * Trg_MilkProd 
    else:
        An_Ca_l = (0.295 + 0.239 * Trg_MilkTPp) * Trg_MilkProd
    # Line 2969 - this is not possible for An_Ca_l to be NA, but keeping commented out for record of R code line number:
    # if math.isnan(An_Ca_l):
    #     An_Ca_l = 0
    return An_Ca_l


def calculate_An_Ca_Clf(An_BW_empty: float, Body_Gain_empty: float) -> float:
    """
    An_Ca_Clf: Ca requirement for calves, g/d 
    """
    An_Ca_Clf = (0.0127 * An_BW_empty + (14.4 * (An_BW_empty**-0.139) * Body_Gain_empty)) / 0.73
    return An_Ca_Clf


def calculate_An_Ca_req(An_StatePhys: str, Dt_DMIn_ClfLiq: float, An_Ca_Clf: float, Fe_Ca_m: float, An_Ca_g: float, An_Ca_y: float, An_Ca_l: float) -> float:
    """
    An_Ca_req: Calcium requirement, g/d
    """
    if An_StatePhys == 'Calf' and Dt_DMIn_ClfLiq > 0:
        An_Ca_req = An_Ca_Clf
    else:
        An_Ca_req = Fe_Ca_m + An_Ca_g + An_Ca_y + An_Ca_l
    return An_Ca_req


def calculate_An_Ca_bal(Abs_CaIn: float, An_Ca_req: float) -> float:
    """
    An_Ca_bal: Calcium balcance, g/d
    """
    An_Ca_bal = Abs_CaIn - An_Ca_req    # Line 2973
    return An_Ca_bal


def calculate_An_Ca_prod(An_Ca_y: float, An_Ca_l: float, An_Ca_g: float) -> float:
    """
    An_Ca_prod: Calcium used for production? (gestation + lactation + growth), g/d
    """
    An_Ca_prod = An_Ca_y + An_Ca_l + An_Ca_g    # Line 2974
    return An_Ca_prod


### PHOSPHORUS ###
def calculate_Ur_P_m(An_BW: float) -> float:
    """
    Ur_P_m: Uriniary phosphorus loss?, g/d, part of maintenance requirement
    """
    Ur_P_m = 0.0006 * An_BW # Line 2977
    return Ur_P_m


def calculate_Fe_P_m(An_Parity_rl: int, An_DMIn: float) -> float:
    """
    Fe_P_m: Fecal P loss?, g/d, part of maintenance requirement
    """
    if An_Parity_rl == 0:   # Line 2978
        Fe_P_m = 0.8 * An_DMIn
    else:
        Fe_P_m = 1.0 * An_DMIn
    return Fe_P_m


def calculate_An_P_m(Ur_P_m: float, Fe_P_m: float) -> float:
    """
    An_P_m: P requirement, g/d
    """
    An_P_m = Ur_P_m + Fe_P_m    # Line 2979
    return An_P_m


def calculate_An_P_g(An_BW_mature: float, An_BW: float, Body_Gain: float) -> float:
    """
    An_P_g: P requirement for growth
    """
    An_P_g = (1.2 + (4.635 * An_BW_mature**.22 * An_BW**-0.22)) * Body_Gain # Line 2980
    return An_P_g


def calculate_An_P_y(An_GestDay: int, An_BW: float) -> float:
    """
    An_P_y: P gestation requirement, g/d
    """
    An_P_y = (0.02743 * math.exp((0.05527 - 0.000075 * An_GestDay) * An_GestDay)    # Line 2981
             - 0.02743 * math.exp((0.05527 - 0.000075 * (An_GestDay - 1)) * (An_GestDay - 1))) * An_BW / 715
    return An_P_y


def calculate_An_P_l(Trg_MilkProd: float, MlkNP_Milk: float) -> float:
    """
    An_P_l: P requirement for lactation, g/d
    """
    if Trg_MilkProd is None or math.isnan(Trg_MilkProd):    # Line 2983
        An_P_l = 0      # If MTP not known then 0.9*Milk
    else:
        An_P_l = (0.48 + 0.13 * MlkNP_Milk * 100) * Trg_MilkProd
    return An_P_l


def calculate_An_P_Clf(An_BW_empty: float, Body_Gain_empty: float) -> float:
    """
    An_P_Clf: P requirement for calves, g/d
    """
    An_P_Clf = (0.0118 * An_BW_empty + (5.85 * (An_BW_empty**-0.027) * Body_Gain_empty)) / 0.65 # Line 2985
    return An_P_Clf


def calculate_An_P_req(An_StatePhys: str, Dt_DMIn_ClfLiq: float, An_P_Clf: float, An_P_m: float, An_P_g: float, An_P_y: float, An_P_l: float) -> float:
    """
    An_P_req: P requirement, g/d
    """
    if An_StatePhys == 'Calf' and Dt_DMIn_ClfLiq > 0:    # LIne 2986-2987
        An_P_req = An_P_Clf
    else:
        An_P_req = An_P_m + An_P_g + An_P_y + An_P_l
    return An_P_req


def calculate_An_P_bal(Abs_PIn: float, An_P_req: float) -> float:
    """
    An_P_bal: P balance, g/d
    """
    An_P_bal = Abs_PIn - An_P_req   # Infused P not currently considered as an input, but should be, Line 2988
    return An_P_bal


def calculate_Fe_P_g(Dt_PIn: float, An_P_l: float, An_P_y: float, An_P_g: float, Ur_P_m: float) -> float:
    """
    Fe_P_g: Fecal P loss, g/d
    """
    Fe_P_g = Dt_PIn - An_P_l - An_P_y - An_P_g - Ur_P_m # Line 2990
    #urinary losses will be underestimated at very high dietary P. Ordinarily 99% by feces.
    return Fe_P_g


def calculate_An_P_prod(An_P_y: float, An_P_l: float, An_P_g: float) -> float:
    """
    An_P_prod: P requirement for production? g/d
    """
    An_P_prod = An_P_y + An_P_l + An_P_g    # Line 2992
    return An_P_prod


### MAGNESIUM ###
def calculate_An_Mg_Clf(An_BW_empty: float, Body_Gain_empty: float) -> float:
    """
    An_Mg_Clf: Mg requirement for calves, g/d
    """
    An_Mg_Clf = (0.0035 * An_BW_empty + (0.60 * (An_BW_empty**-0.036) * Body_Gain_empty)) / 0.30    # Line 2995
    return An_Mg_Clf


def calculate_Ur_Mg_m(An_BW: float) -> float:
    """
    Ur_Mg_m: Urine Mg loss, g/d
    """
    Ur_Mg_m = 0.0007 * An_BW    # Line 2996
    return Ur_Mg_m


def calculate_Fe_Mg_m(An_DMIn: float) -> float:
    """
    Fe_Mg_m: Fecal Mg loss, g/d
    """
    Fe_Mg_m = 0.3 * An_DMIn # Line 2997
    return Fe_Mg_m


def calculate_An_Mg_m(Ur_Mg_m: float, Fe_Mg_m: float) -> float:
    """
    An_Mg_m: Mg maintenance requirement, g/d
    """
    An_Mg_m = Ur_Mg_m + Fe_Mg_m # Line 2998
    return An_Mg_m


def calculate_An_Mg_g(Body_Gain: float) -> float:
    """
    An_Mg_g: Mg requirement for gestation, g/d
    """
    An_Mg_g = 0.45 * Body_Gain  # Line 2999
    return An_Mg_g


def calculate_An_Mg_y(An_GestDay: int, An_BW: float) -> float:
    """
    An_Mg_y: Mg requirement for gestation, g/d
    """
    if An_GestDay > 190:    # Line 3000
        An_Mg_y = 0.3 * (An_BW / 715)
    else:
        An_Mg_y = 0
    return An_Mg_y


def calculate_An_Mg_l(Trg_MilkProd: float) -> float:
    """
    An_Mg_l: Mg requirement for lactation
    """
    if Trg_MilkProd is None or math.isnan(Trg_MilkProd):    # Line 3001
        An_Mg_l = 0
    else:
        An_Mg_l = 0.11 * Trg_MilkProd
    return An_Mg_l


def calculate_An_Mg_req(An_StatePhys: str, Dt_DMIn_ClfLiq: float, An_Mg_Clf: float, An_Mg_m: float, An_Mg_g: float, An_Mg_y: float, An_Mg_l: float) -> float:
    """
    An_Mg_req: Mg requirement, g/d
    """
    if An_StatePhys == 'Calf' and Dt_DMIn_ClfLiq > 0:   # Line 3002
        An_Mg_req = An_Mg_Clf
    else:
        An_Mg_req = An_Mg_m + An_Mg_g + An_Mg_y + An_Mg_l
    return An_Mg_req


def calculate_An_Mg_bal(Abs_MgIn: float, An_Mg_req: float) -> float:
    """
    An_Mg_bal: Mg balance, g/d
    """
    An_Mg_bal = Abs_MgIn - An_Mg_req    # Line 3004
    return An_Mg_bal


def calculate_An_Mg_prod(An_Mg_y: float, An_Mg_l: float, An_Mg_g: float) -> float:
    """
    An_Mg_prod: Mg for production?, g/d
    """
    An_Mg_prod = An_Mg_y + An_Mg_l + An_Mg_g    # Line 3005
    return An_Mg_prod


### SODIUM ###
def calculate_An_Na_Clf(An_BW_empty: float, Body_Gain_empty: float) -> float:
    """
    An_Na_Clf: Na requirement calves, g/d
    """
    An_Na_Clf = (0.00637 * An_BW_empty + (1.508 * (An_BW_empty**-0.045) * Body_Gain_empty)) / 0.24  # Line 3008
    return An_Na_Clf


def calculate_Fe_Na_m(An_DMIn: float) -> float:
    """
    Fe_Na_m: Fecal Na loss, g/d
    """
    Fe_Na_m = 1.45 * An_DMIn    # Line 3009
    return Fe_Na_m


def calculate_An_Na_g(Body_Gain: float) -> float:
    """
    An_Na_g: Na required for growth, g/d 
    """
    An_Na_g = 1.4 * Body_Gain   # Line 3010
    return An_Na_g


def calculate_An_Na_y(An_GestDay: int, An_BW: float) -> float:
    """
    An_Na_y: Na required for gestation
    """
    if An_GestDay > 190:    # Line 3011
        An_Na_y = 1.4 * An_BW / 715
    else:
        An_Na_y = 0
    return An_Na_y


def calculate_An_Na_l(Trg_MilkProd: float) -> float:
    """
    An_Na_l: Na requirement for lactation, g/d
    """
    if Trg_MilkProd is None or math.isnan(Trg_MilkProd):    # Line 3012
        An_Na_l = 0
    else:
        An_Na_l = 0.4 * Trg_MilkProd
    return An_Na_l


def calculate_An_Na_req(An_StatePhys: str, Dt_DMIn_ClfLiq: float, An_Na_Clf: float, Fe_Na_m: float, An_Na_g: float, An_Na_y: float, An_Na_l: float) -> float:
    """
    An_Na_req: Na requirement, g/d
    """
    if An_StatePhys == 'Calf' and Dt_DMIn_ClfLiq > 0:   # Line 3013-3014
        An_Na_req = An_Na_Clf
    else:
        An_Na_req = Fe_Na_m + An_Na_g + An_Na_y + An_Na_l
    return An_Na_req


def calculate_An_Na_bal(Abs_NaIn: float, An_Na_req: float) -> float:
    """
    An_Na_bal: Na balance, g/d
    """
    An_Na_bal = Abs_NaIn - An_Na_req    # Line 3015
    return An_Na_bal


def calculate_An_Na_prod(An_Na_y: float, An_Na_l: float, An_Na_g: float) -> float:
    """
    An_Na_prod: Na for production?, g/d
    """
    An_Na_prod = An_Na_y + An_Na_l + An_Na_g    # Line 3016
    return An_Na_prod


### CHLORINE ###
def calculate_An_Cl_Clf(An_BW_empty: float, Body_Gain_empty: float) -> float:
    """
    An_Cl_Clf: Cl requirement for calves, g/d
    """
    An_Cl_Clf = 0.8 * (0.00637 * An_BW_empty + (1.508 * (An_BW_empty**-0.045) * Body_Gain_empty)) / 0.24    # Line 3018 
    return An_Cl_Clf


def calculate_Fe_Cl_m(An_DMIn: float) -> float:
    """
    Fe_Cl_m: Fecal Cl loss, g/d
    """
    Fe_Cl_m = 1.11 * An_DMIn    # line 3019
    return Fe_Cl_m


def calculate_An_Cl_g(Body_Gain: float) -> float:
    """
    An_Cl_g: Cl required for growth, g/d
    """
    An_Cl_g = 1.0 * Body_Gain   # Line 3020
    return An_Cl_g


def calculate_An_Cl_y(An_GestDay: int, An_BW: float) -> float:
    """
    An_Cl_y: Cl requirement for gestation, g/d
    """
    if An_GestDay > 190:    # Line 3021
        An_Cl_y = 1.0 * An_BW / 715       
    else:
       An_Cl_y = 0
    return An_Cl_y


def calculate_An_Cl_l(Trg_MilkProd: float) -> float:
    """
    An_Cl_l: Cl required for lactation, g/d
    """
    if Trg_MilkProd is None or math.isnan(Trg_MilkProd):    # Line 3022
        An_Cl_l = 0
    else:
        An_Cl_l = 1.0 * Trg_MilkProd
    return An_Cl_l


def calculate_An_Cl_req(An_StatePhys: str, Dt_DMIn_ClfLiq: float, An_Cl_Clf: float, Fe_Cl_m: float, An_Cl_g: float, An_Cl_y: float, An_Cl_l: float) -> float:
    """
    An_Cl_req: Cl requirement, g/d
    """
    if An_StatePhys == 'Calf' and Dt_DMIn_ClfLiq > 0:   # Line 3023-3024
        An_Cl_req = An_Cl_Clf
    else:
        An_Cl_req = Fe_Cl_m + An_Cl_g + An_Cl_y + An_Cl_l
    return An_Cl_req


def calculate_An_Cl_bal(Abs_ClIn: float, An_Cl_req: float) -> float:
    """
    An_Cl_bal: Cl balance, g/d
    """
    An_Cl_bal = Abs_ClIn - An_Cl_req    # Line 3025
    return An_Cl_bal


def calculate_An_Cl_prod(An_Cl_y: float, An_Cl_l: float, An_Cl_g: float) -> float:
    """
    An_Cl_prod: Cl required for production?, g/d
    """
    An_Cl_prod = An_Cl_y + An_Cl_l + An_Cl_g    # Line 3026
    return An_Cl_prod


### POTASSIUM ###
def calculate_An_K_Clf(An_BW_empty: float, Body_Gain_empty: float) -> float:
    """
    An_K_Clf: K required for calves, g/d
    """
    An_K_Clf = (0.0203 * An_BW_empty + (1.14 * (An_BW_empty**-0.048) * Body_Gain_empty)) / 0.13 # Line 3028 
    return An_K_Clf


def calculate_Ur_K_m(Trg_MilkProd: float, An_BW: float) -> float:
    """
    Ur_K_m: Urinary K loss, g/d
    """
    if Trg_MilkProd > 0:    # Line 3029
        Ur_K_m = 0.2 * An_BW
    else:
        Ur_K_m = 0.07 * An_BW
    return Ur_K_m


def calculate_Fe_K_m(An_DMIn: float) -> float:
    """
    Fe_K_m: Fecal K requirement, g/d
    """
    Fe_K_m = 2.5 * An_DMIn  # Line 3030
    return Fe_K_m


def calculate_An_K_m(Ur_K_m: float, Fe_K_m: float) -> float:
    """
    An_K_m: K required for maintenance, g/d
    """
    An_K_m = Ur_K_m + Fe_K_m    # Line 3031
    return An_K_m


def calculate_An_K_g(Body_Gain: float) -> float:
    """
    An_K_g: K requirement for growth, g/d
    """
    An_K_g = 2.5 * Body_Gain    # Line 3032
    return An_K_g


def calculate_An_K_y(An_GestDay: int, An_BW: float) -> float:
    """
    An_K_y: K required for gestation, g/d
    """
    if An_GestDay > 190:    # Line 3033
        An_K_y = 1.03 * An_BW / 715
    else:
        An_K_y = 0
    return An_K_y


def calculate_An_K_l(Trg_MilkProd: float) -> float:
    """
    An_K_l: K required for lactation, g/d
    """
    if Trg_MilkProd is None or math.isnan(Trg_MilkProd):    # Line 3034
        An_K_l = 0
    else:
        An_K_l = 1.5 * Trg_MilkProd
    return An_K_l


def calculate_An_K_req(An_StatePhys: str, Dt_DMIn_ClfLiq: float, An_K_Clf: float, An_K_m: float, An_K_g: float, An_K_y: float, An_K_l: float) -> float:
    """
    An_K_req: K requirement, g/d
    """
    if An_StatePhys == 'Calf' and Dt_DMIn_ClfLiq > 0:   # Line 3035-3036
        An_K_req = An_K_Clf
    else: 
        An_K_req = An_K_m + An_K_g + An_K_y + An_K_l
    return An_K_req


def calculate_An_K_bal(Abs_KIn: float, An_K_req: float) -> float:
    """
    An_K_bal: K balance, g/d
    """ 
    An_K_bal = Abs_KIn - An_K_req   # Line 3037
    return An_K_bal


def calculate_An_K_prod(An_K_y: float, An_K_l: float, An_K_g: float) -> float:
    """
    An_K_prod: K for production?, g/d
    """
    An_K_prod = An_K_y + An_K_l + An_K_g    # Line 3038
    return An_K_prod


### SULPHUR ###
def calculate_An_S_req(An_DMIn: float) -> float:
    """
    An_S_req: S requirement, g/d
    """
    An_S_req = 2 * An_DMIn  # Line 3040
    return An_S_req


def calculate_An_S_bal(Dt_SIn: float, An_S_req: float) -> float:
    """
    An_S_bal: S balance, g/d
    """
    An_S_bal = Dt_SIn - An_S_req    # Line 3041
    return An_S_bal


### COBALT ###
def calculate_An_Co_req(An_DMIn: float) -> float:
    """
    An_Co_req: Cobalt requirement, mg/d
    """
    An_Co_req = 0.2 * An_DMIn  # Based on dietary intake assuming no absorption for a calf, Line 3046
    return An_Co_req


def calculate_An_Co_bal(Abs_CoIn: float, An_Co_req: float) -> float:
    """
    An_Co_bal: Co balance, mg/d 
    """
    An_Co_bal = Abs_CoIn - An_Co_req # calf absorption set to 0 and other StatePhys to 1 above, Line 3047
    return An_Co_bal


### COPPER ###
def calculate_An_Cu_Clf(An_BW: float, Body_Gain_empty: float) -> float:
    """
    An_Cu_Clf: Cu requirement for calves, mg/d
    """
    An_Cu_Clf = (0.0145 * An_BW + 2.5 * Body_Gain_empty) / 0.5  # Line 3050
    return An_Cu_Clf


def calculate_An_Cu_m(An_BW: float) -> float:
    """
    An_Cu_m: Cu maintenance requirement
    """
    An_Cu_m = 0.0145 * An_BW    # Line 3051
    return An_Cu_m


def calculate_An_Cu_g(Body_Gain: float) -> float:
    """
    An_Cu_g: Cu required for growth, ,g/d
    """
    An_Cu_g = 2.0 * Body_Gain   # Line 3052
    return An_Cu_g


def calculate_An_Cu_y(An_GestDay: int, An_BW: float) -> float:
    """
    An_Cu_y: Cu required for gestation, mg/d
    """
    if An_GestDay < 90: # Line 3053
        An_Cu_y = 0
    elif An_GestDay > 190:
        An_Cu_y = 0.0023 * An_BW
    else:
        An_Cu_y = 0.0003 * An_BW
    return An_Cu_y


def calculate_An_Cu_l(Trg_MilkProd: float) -> float:
    """
    An_Cu_l: Cu required for lactation, mg/d
    """
    if Trg_MilkProd is None or math.isnan(Trg_MilkProd):    # Line 3054
        An_Cu_l = 0
    else:
        An_Cu_l = 0.04 * Trg_MilkProd
    return An_Cu_l


def calculate_An_Cu_req(An_StatePhys: str, Dt_DMIn_ClfLiq: float, An_Cu_Clf: float, An_Cu_m: float, An_Cu_g: float, An_Cu_y: float, An_Cu_l: float) -> float:
    """
    An_Cu_req: Cu requirement, mg/d
    """
    if An_StatePhys == 'Calf' and Dt_DMIn_ClfLiq > 0:   # Line 3055-3056
        An_Cu_req = An_Cu_Clf
    else:
        An_Cu_req = An_Cu_m + An_Cu_g + An_Cu_y + An_Cu_l
    return An_Cu_req


def calculate_An_Cu_bal(Abs_CuIn: float, An_Cu_req: float) -> float:
    """
    An_Cu_bal: Cu balance, mg/d
    """
    An_Cu_bal = Abs_CuIn - An_Cu_req    # Line 3057
    return An_Cu_bal


def calculate_An_Cu_prod(An_Cu_y: float, An_Cu_l: float, An_Cu_g: float) -> float:
    """
    An_Cu_prod: Cu for production?, mg/d
    """
    An_Cu_prod = An_Cu_y + An_Cu_l + An_Cu_g    # Line 3058
    return An_Cu_prod


### IODINE ###
def calculate_An_I_req(An_StatePhys: str, An_DMIn: float, An_BW: float, Trg_MilkProd: float) -> float:
    """
    An_I_req: I requirement, mg/d
    """
    if An_StatePhys == 'Calf':  # Line 3060
        An_I_req = 0.8 * An_DMIn
    else:
        An_I_req = 0.216 * An_BW**0.528 + 0.1 * Trg_MilkProd
    return An_I_req


def calculate_An_I_bal(Dt_IIn: float, An_I_req: float) -> float:
    """
    An_I_bal: I balance, mg/d
    """
    An_I_bal = Dt_IIn - An_I_req    # Line 3061
    return An_I_bal


### IRON ### 
def calculate_An_Fe_Clf(Body_Gain: float) -> float:
    """
    An_Fe_Clf: Fe requirement for calves, mg/d
    """
    An_Fe_Clf = 34 * Body_Gain / 0.25   # Line 3064
    return An_Fe_Clf


def calculate_An_Fe_g(Body_Gain: float) -> float:
    """
    An_Fe_g: Fe requirement for growth, mg/d
    """
    An_Fe_g = 34 * Body_Gain    # Line 3065
    return An_Fe_g


def calculate_An_Fe_y(An_GestDay: int, An_BW: float) -> float:
    """
    An_Fe_y: Fe required for gestation, mg/d
    """
    if An_GestDay > 190:    # Line 3066
        An_Fe_y = 0.025 * An_BW
    else:
        An_Fe_y = 0
    return An_Fe_y


def calculate_An_Fe_l(Trg_MilkProd: float) -> float:
    """
    An_Fe_l: Fe required for lactation, mg/d
    """
    if Trg_MilkProd is None or math.isnan(Trg_MilkProd):    # Line 3067
       An_Fe_l = 0
    else:
        An_Fe_l = 1.0 * Trg_MilkProd
    return An_Fe_l


def calculate_An_Fe_req(An_StatePhys: str, Dt_DMIn_ClfLiq: float, An_Fe_Clf: float, An_Fe_g: float, An_Fe_y: float, An_Fe_l: float) -> float:
    """
    An_Fe_req: Fe requirement, mg/d
    There's a comment in the R code saying: #add An_Fe_m when I move the eqn up here.
    Also includes Line 3290; An_Fe_m <- 0  #no Fe maintenance requirement
    """
    if An_StatePhys == 'Calf' and Dt_DMIn_ClfLiq > 0:   # Line 3068-3069
        An_Fe_req = An_Fe_Clf
    else: 
        An_Fe_req = An_Fe_g + An_Fe_y + An_Fe_l
    return An_Fe_req


def calculate_An_Fe_bal(Abs_FeIn: float, An_Fe_req: float) -> float:
    """
    An_Fe_bal: Fe balance, mg/d
    """
    An_Fe_bal = Abs_FeIn - An_Fe_req    # Line 3070
    return An_Fe_bal


def calculate_An_Fe_prod(An_Fe_y: float, An_Fe_l: float, An_Fe_g: float) -> float:
    """
    An_Fe_prod: Fe required for production?, mg/d
    """
    An_Fe_prod = An_Fe_y + An_Fe_l + An_Fe_g    # Line 3071
    return An_Fe_prod


### MANGANESE ###
def calculate_An_Mn_Clf(An_BW: float, Body_Gain: float) -> float:
    """
    An_Mn_Clf: Mn requirement for calves, mg/d
    """
    An_Mn_Clf = (0.0026 * An_BW + 0.7 * Body_Gain) / 0.01   # Line 3073
    return An_Mn_Clf


def calculate_An_Mn_m(An_BW: float) -> float:
    """
    An_Mn_m: Mn required for maintenance, mg/d
    """
    An_Mn_m = 0.0026 * An_BW    # Line 3074
    return An_Mn_m


def calculate_An_Mn_g(Body_Gain: float) -> float:
    """
    An_Mn_g: Mn required for growth, mg/d
    """
    An_Mn_g = 0.7 * Body_Gain   # Line 3075
    return An_Mn_g


def calculate_An_Mn_y(An_GestDay: int, An_BW: float) -> float:
    """
    An_Mn_y: Mn required for gestation, mg/d
    """
    if An_GestDay > 190:    # Line 3076
        An_Mn_y = 0.00042 * An_BW
    else:
        An_Mn_y = 0
    return An_Mn_y


def calculate_An_Mn_l(Trg_MilkProd: float) -> float:
    """
    An_Mn_l: Mn required for lactation, mg/d
    """
    if Trg_MilkProd is None or math.isnan(Trg_MilkProd):    # Line 3077
       An_Mn_l = 0
    else:
        An_Mn_l = 0.03 * Trg_MilkProd
    return An_Mn_l


def calculate_An_Mn_req(An_StatePhys: str, Dt_DMIn_ClfLiq: float, An_Mn_Clf: float, An_Mn_m: float, An_Mn_g: float, An_Mn_y: float, An_Mn_l: float) -> float:
    """
    An_Mn_req: Mn requirement, mg/d
    """
    if An_StatePhys == 'Calf' and Dt_DMIn_ClfLiq > 0:   # Line 3078 
        An_Mn_req = An_Mn_Clf
    else: 
        An_Mn_req = An_Mn_m + An_Mn_g + An_Mn_y + An_Mn_l
    return An_Mn_req


def calculate_An_Mn_bal(Abs_MnIn: float, An_Mn_req: float) -> float:
    """
    An_Mn_bal: Mn balance, mg/d
    """
    An_Mn_bal = Abs_MnIn - An_Mn_req    # Line 3080
    return An_Mn_bal


def calculate_An_Mn_prod(An_Mn_y: float, An_Mn_l: float, An_Mn_g: float) -> float:
    """
    An_Mn_prod: Mn required for production?, mg/d
    """
    An_Mn_prod = An_Mn_y + An_Mn_l + An_Mn_g    # Line 3081
    return An_Mn_prod


### SELENIUM ###
def calculate_An_Se_req(An_DMIn: float) -> float:
    """
    An_Se_req: Se requirement
    """
    An_Se_req = 0.3 * An_DMIn   # Line 3083
    return An_Se_req


def calculate_An_Se_bal(Dt_SeIn: float, An_Se_req: float) -> float:
    """
    An_Se_bal: Se balance, mg/d
    """
    An_Se_bal = Dt_SeIn - An_Se_req # Line 3084
    return An_Se_bal


### ZINC ###
def calculate_An_Zn_Clf(An_DMIn: float, Body_Gain: float) -> float:
    """
    An_Zn_Clf: Zn requirement fro calves, mg/d
    """
    An_Zn_Clf = (2.0 * An_DMIn + 24 * Body_Gain) / 0.25 # Line 3087 
    return An_Zn_Clf


def calculate_An_Zn_m(An_DMIn: float) -> float:
    """
    An_Zn_m: Zn requirement for maintenance, mg/d
    """
    An_Zn_m = 5.0 * An_DMIn # Line 3088
    return An_Zn_m


def calculate_An_Zn_g(Body_Gain: float) -> float:
    """
    An_Zn_g: Zn required for growth, mg/d
    """
    An_Zn_g = 24 * Body_Gain    # Line 3089
    return An_Zn_g


def calculate_An_Zn_y(An_GestDay: int, An_BW: float) -> float:
    """
    An_Zn_y: Zn required for gestation, mg/d
    """
    if An_GestDay > 190:    # Line 3090
        An_Zn_y = 0.017 * An_BW
    else:
        An_Zn_y = 0
    return An_Zn_y


def calculate_An_Zn_l(Trg_MilkProd: float) -> float:
    """
    An_Zn_l: Zn requirement for lactation, mg/d
    """
    if Trg_MilkProd is None or math.isnan(Trg_MilkProd):    # Line 3091
       An_Zn_l = 0
    else:
        An_Zn_l = 4.0 * Trg_MilkProd
    return An_Zn_l


def calculate_An_Zn_req(An_StatePhys: str, Dt_DMIn_ClfLiq: float, An_Zn_Clf: float, An_Zn_m: float, An_Zn_g: float, An_Zn_y: float, An_Zn_l: float) -> float:
    """
    An_Zn_req: Zn requirement, mg/d
    """
    if An_StatePhys == 'Calf' and Dt_DMIn_ClfLiq > 0:   # Line 3092-3093
        An_Zn_req = An_Zn_Clf
    else: 
        An_Zn_req = An_Zn_m + An_Zn_g + An_Zn_y + An_Zn_l
    return An_Zn_req


def calculate_An_Zn_bal(Abs_ZnIn: float, An_Zn_req: float) -> float:
    """
    An_Zn_bal: Zn balance, mg/d
    """
    An_Zn_bal = Abs_ZnIn - An_Zn_req    # Line 3094
    return An_Zn_bal


def calculate_An_Zn_prod(An_Zn_y: float, An_Zn_l: float, An_Zn_g: float) -> float:
    """
    An_Zn_prod: Zn required for production, mg/d
    """
    An_Zn_prod = An_Zn_y + An_Zn_l + An_Zn_g    # Line 3095
    return An_Zn_prod

### DCAD ###
def calculate_An_DCADmeq(Dt_K: float, Dt_Na: float, Dt_Cl: float, Dt_S: float) -> float:
    """
    An_DCADmeq: DCAD, meg/kg? Should this be meq/kg?
    """
    An_DCADmeq = (Dt_K / 0.039 + Dt_Na / 0.023 - Dt_Cl / 0.0355 - Dt_S / 0.016) * 10    # #DCAD in meg/kg, Line 3096
    return An_DCADmeq
