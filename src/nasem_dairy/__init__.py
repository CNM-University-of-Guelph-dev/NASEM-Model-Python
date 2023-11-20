# read version from installed package
from importlib.metadata import version
__version__ = version("nasem_dairy")


from nasem_dairy.ration_balancer.ration_balancer_functions import fl_get_rows, get_nutrient_intakes, fl_get_feed_rows, read_input, check_coeffs_in_coeff_dict, read_csv_input, NDF_precalculation
from nasem_dairy.ration_balancer.execute_model import NASEM_model
from nasem_dairy.NASEM_equations.misc_equations import AA_calculations, calculate_GrUter_BWgain
from nasem_dairy.NASEM_equations.Du_microbial_equations import calculate_Du_MiN_g, calculate_Du_MiN_NRC2021_g, calculate_Du_MiN_VTln_g, calculate_Du_MiN_VTnln_g
from nasem_dairy.NASEM_equations.Animal_supply_equations import calculate_An_DEIn, calculate_An_NE
from nasem_dairy.NASEM_equations.Milk_equations import calculate_Mlk_Fat_g, calculate_Mlk_NP_g, calculate_Mlk_Prod_comp, calculate_Mlk_Prod_MPalow, calculate_Mlk_Prod_NEalow, check_animal_lactation_day, calculate_An_MPIn_g
from nasem_dairy.NASEM_equations.ME_equations import calculate_ME_requirement, calculate_An_MEgain, calculate_An_MEmUse, calculate_Gest_MEuse, calculate_Trg_Mlk_MEout
from nasem_dairy.NASEM_equations.MP_equations import calculate_MP_requirement, calculate_An_MPm_g_Trg, calculate_Body_MPuse_g_Trg, calculate_Gest_MPuse_g_Trg, calculate_Mlk_MPuse_g_Trg
from nasem_dairy.ration_balancer.coeff_dict import coeff_dict
from nasem_dairy.NASEM_equations.DMI_equations import dry_cow_equations, heifer_growth
from nasem_dairy.NASEM_equations.micronutrient_equations import mineral_intakes, vitamin_supply, mineral_requirements
from nasem_dairy.NASEM_equations.temporary_functions import temp_MlkNP_Milk, temp_calc_An_DigTPaIn, temp_calc_An_GasEOut, calculate_Mlk_Prod, calculate_MlkNE_Milk, calculate_Mlk_MEout

from nasem_dairy.NASEM_equations.dev_DMI_equations import (
    calculate_Kb_LateGest_DMIn,
    calculate_An_PrePartWklim,
    calculate_Dt_DMIn_Heif_LateGestInd,
    calculate_Dt_DMIn_Heif_LateGestPen,
    calculate_Dt_NDFdev_DMI,
    calculate_Dt_DMIn_Heif_NRCa,
    calculate_Dt_DMIn_Heif_NRCad,
    calculate_Dt_DMIn_Heif_H1,
    calculate_Dt_DMIn_Heif_H2,
    calculate_Dt_DMIn_Heif_HJ1,
    calculate_Dt_DMIn_Heif_HJ2,
    calculate_Dt_DMIn_Lact1,
    calculate_Dt_DMIn_BW_LateGest_i,
    calculate_Dt_DMIn_BW_LateGest_p,
    calculate_Dt_DMIn_DryCow1_FarOff,
    calculate_Dt_DMIn_DryCow1_Close,
    calculate_Dt_DMIn_DryCow2
)
from nasem_dairy.NASEM_equations.dev_milk_equations import calculate_Trg_NEmilk_Milk
