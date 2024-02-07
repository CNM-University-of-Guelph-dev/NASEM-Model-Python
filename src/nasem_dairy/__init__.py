# read version from installed package
from importlib.metadata import version
__version__ = version("nasem_dairy")


from nasem_dairy.ration_balancer.ration_balancer_functions import fl_get_rows, get_nutrient_intakes, fl_get_feed_rows, read_input, check_coeffs_in_coeff_dict, read_csv_input, read_infusion_input
from nasem_dairy.ration_balancer.execute_model import NASEM_model
from nasem_dairy.NASEM_equations.dev_gestation_equations import calculate_GrUter_BWgain
from nasem_dairy.NASEM_equations.Animal_supply_equations import calculate_An_DEIn, calculate_An_NE
from nasem_dairy.NASEM_equations.Milk_equations import calculate_Mlk_Fat_g, calculate_Mlk_Prod_comp, calculate_Mlk_Prod_MPalow, calculate_Mlk_Prod_NEalow, check_animal_lactation_day
from nasem_dairy.NASEM_equations.MP_equations import calculate_MP_requirement, calculate_An_MPm_g_Trg, calculate_Body_MPuse_g_Trg, calculate_Gest_MPuse_g_Trg, calculate_Mlk_MPuse_g_Trg
from nasem_dairy.ration_balancer.default_values_dictionaries import coeff_dict, infusion_dict, MP_NP_efficiency_dict
from nasem_dairy.NASEM_equations.micronutrient_equations import mineral_requirements
from nasem_dairy.NASEM_equations.temporary_functions import temp_MlkNP_Milk, temp_calc_An_DigTPaIn, calculate_Mlk_Prod, calculate_MlkNE_Milk, calculate_Mlk_MEout

# Import statements for updated functions
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

from nasem_dairy.NASEM_equations.dev_milk_equations import (
    calculate_Trg_NEmilk_Milk,
    calculate_Mlk_NP_g,
    calculate_Mlk_CP_g
)

from nasem_dairy.NASEM_equations.dev_nutrient_intakes import (
    calculate_TT_dcFdNDF_Lg,
    calculate_Fd_DNDF48,
    calculate_TT_dcFdNDF_48h,
    calculate_TT_dcFdNDF_Base,
    calculate_Fd_GE,
    calculate_Fd_DMIn,
    calculate_Fd_AFIn,
    calculate_Fd_For,
    calculate_Fd_ForWet,
    calculate_Fd_ForDry,
    calculate_Fd_Past,
    calculate_Fd_LiqClf,
    calculate_Fd_ForNDF,
    calculate_Fd_NDFnf,
    calculate_Fd_NPNCP,
    calculate_Fd_NPN,
    calculate_Fd_NPNDM,
    calculate_Fd_TP,
    calculate_Fd_fHydr_FA,
    calculate_Fd_FAhydr,
    calculate_Fd_NFC,
    calculate_Fd_rOM,
    calculate_Fd_GEIn,
    calculate_Fd_DigNDFIn_Base,
    calculate_Fd_NPNCPIn,
    calculate_Fd_NPNIn,
    calculate_Fd_NPNDMIn,
    calculate_Fd_CPAIn,
    calculate_Fd_CPBIn,
    calculate_Fd_CPBIn_For,
    calculate_Fd_CPBIn_Conc,
    calculate_Fd_CPCIn,
    calculate_Fd_CPIn_ClfLiq,
    calculate_Fd_CPIn_ClfDry,
    calculate_Fd_rdcRUPB,
    calculate_Fd_RUPBIn,
    calculate_Fd_RUPIn,
    calculate_Fd_RUP_CP,
    calculate_Fd_RUP,
    calculate_Fd_RDP,
    calculate_Fd_OMIn,
    calculate_Fd_DE_base_1,
    calculate_Fd_DE_base_2,
    calculate_Fd_DE_base,
    calculate_Fd_DEIn_base,
    calculate_Fd_DEIn_base_ClfLiq,
    calculate_Fd_DEIn_base_ClfDry,
    calculate_Fd_DMIn_ClfLiq,
    calculate_Fd_DE_ClfLiq,
    calculate_Fd_ME_ClfLiq,
    calculate_Fd_DMIn_ClfFor,
    calculate_Fd_PinorgIn,
    calculate_Fd_PorgIn,
    calculate_Fd_MgIn_min,
    calculate_Fd_acCa,
    calculate_Fd_acPtot,
    calculate_Fd_acMg,
    calculate_Fd_acNa,
    calculate_Fd_acK,
    calculate_Fd_acCl,
    calculate_Fd_absCaIn,
    calculate_Fd_absPIn,
    calculate_Fd_absMgIn_base,
    calculate_Fd_absNaIn,
    calculate_Fd_absKIn,
    calculate_Fd_absClIn,
    calculate_Fd_acCo,
    calculate_Fd_acCu,
    calculate_Fd_acFe,
    calculate_Fd_acMn,
    calculate_Fd_acZn,
    calculate_Fd_DigSt,
    calculate_Fd_DigStIn_Base,
    calculate_Fd_DigrOMt,
    calculate_Fd_idRUPIn,
    calculate_TT_dcFdFA,
    calculate_Fd_DigFAIn,
    calculate_Dt_ForDNDF48,
    calculate_Dt_ForDNDF48_ForNDF,
    calculate_Dt_ADF_NDF,
    calculate_Dt_DE_ClfLiq,
    calculate_Dt_ME_ClfLiq,
    calculate_Dt_NDFnfIn,
    calculate_Dt_Lg_NDF,
    calculate_Dt_ForNDFIn,
    calculate_Dt_PastSupplIn,
    calculate_Dt_NIn,
    calculate_Dt_RUPIn,
    calculate_Dt_RUP_CP,
    calculate_Dt_fCPBdu,
    calculate_Dt_UFAIn,
    calculate_Dt_MUFAIn,
    calculate_Dt_PUFAIn,
    calculate_Dt_SatFAIn,
    calculate_Dt_OMIn,
    calculate_Dt_rOMIn,
    calculate_Dt_DM,
    calculate_Dt_NDFIn_BW,
    calculate_Dt_ForNDF_NDF,
    calculate_Dt_ForNDFIn_BW,
    calculate_Dt_DMInSum,
    calculate_Dt_DEIn_ClfLiq,
    calculate_Dt_MEIn_ClfLiq,
    calculate_Dt_CPA_CP,
    calculate_Dt_CPB_CP,
    calculate_Dt_CPC_CP,
    calculate_Dt_DigNDFIn,
    calculate_Dt_DigStIn,
    calculate_Dt_DigrOMaIn,
    calculate_Dt_dcCP_ClfDry,
    calculate_Dt_DENDFIn,
    calculate_Dt_DEStIn,
    calculate_Dt_DErOMIn,
    calculate_Dt_DigCPaIn,
    calculate_Dt_DECPIn,
    calculate_Dt_DENPNCPIn,
    calculate_Dt_DETPIn,
    calculate_Dt_DEFAIn,
    calculate_Dt_DMIn_ClfStrt,
    calculate_Dt_DEIn,
    calculate_TT_dcNDF_Base,
    calculate_TT_dcNDF,
    calculate_TT_dcSt_Base,
    calculate_TT_dcSt,
    calculate_diet_info,
    calculate_diet_data_initial,
    calculate_diet_data_complete
)

from nasem_dairy.NASEM_equations.dev_rumen_equations import (
    calculate_Rum_dcNDF,
    calculate_Rum_dcSt,
    calculate_Rum_DigNDFIn,
    calculate_Rum_DigStIn
)

from nasem_dairy.NASEM_equations.dev_microbial_protein_equations import (
    calculate_RDPIn_MiNmax,
    calculate_MiN_Vm,
    calculate_Du_MiN_NRC2021_g,
    calculate_Du_MiN_VTln_g,
    calculate_Du_MiN_VTnln_g,
    calculate_Du_MiCP,
    calculate_Du_idMiCP_g,
    calculate_Du_idMiCP,
    calculate_Du_idMiTP_g,
    calculate_Du_idMiTP
)

from nasem_dairy.NASEM_equations.dev_protein_equations import (
    calculate_f_mPrt_max, 
    calculate_Du_MiCP_g, 
    calculate_Du_MiTP_g,
    calculate_Scrf_CP_g
)

from nasem_dairy.NASEM_equations.dev_amino_acid_equations import (
    calculate_Du_AAMic,
    calculate_Du_IdAAMic,
    calculate_Abs_AA_g,
    calculate_mPrtmx_AA,
    calculate_mPrtmx_AA2,
    calculate_AA_mPrtmx,
    calculate_mPrt_AA_01,
    calculate_mPrt_k_AA,
    calculate_Abs_EAA_g,
    calculate_Abs_neAA_g,
    calculate_Abs_OthAA_g,
    calculate_Abs_EAA2_HILKM_g,
    calculate_Abs_EAA2_RHILKM_g,
    calculate_Abs_EAA2_HILKMT_g,
    calculate_Abs_EAA2b_g,
    calculate_mPrt_k_EAA2
)


from nasem_dairy.NASEM_equations.dev_infusion_equations import (
    calculate_Inf_TPIn,
    calculate_Inf_OMIn,
    calculate_Inf_Rum,
    calculate_Inf_SI,
    calculate_Inf_Art,
    calculate_InfRum_TPIn,
    calculate_InfSI_TPIn,
    calculate_InfRum_RUPIn,
    calculate_InfRum_RUP_CP,
    calculate_InfRum_idRUPIn,
    calculate_InfSI_idTPIn,
    calculate_InfSI_idCPIn,
    calculate_Inf_idCPIn,
    calculate_InfRum_RDPIn,
    calculate_Inf_DigFAIn,
    calculate_Inf_DEAcetIn,
    calculate_Inf_DEPropIn,
    calculate_Inf_DEButrIn,
    calculate_infusion_data
)

from nasem_dairy.NASEM_equations.dev_animal_equations import (
    calculate_An_DMIn_BW,
    calculate_An_RDPIn,
    calculate_An_RDP,
    calculate_An_RDPIn_g,
    calculate_An_DMIn_BW,
    calculate_An_NDFIn,
    calculate_An_NDF,
    calculate_An_DigNDFIn,
    calculate_An_DENDFIn,
    calculate_An_DigStIn,
    calculate_An_DEStIn,
    calculate_An_DigrOMaIn,
    calculate_An_DErOMIn,
    calculate_An_idRUPIn,
    calculate_An_RUPIn,
    calculate_An_DMIn,
    calculate_An_CPIn,
    calculate_An_DigNDF,
    calculate_An_GEIn,
    calculate_An_GasEOut_Dry,
    calculate_An_GasEOut_Lact,
    calculate_An_GasEOut_Heif,
    calculate_An_GasEOut,
    calculate_An_DigCPaIn,
    calculate_An_DECPIn,
    calculate_An_DENPNCPIn,
    calculate_An_DETPIn,
    calculate_An_DigFAIn,
    calculate_An_DEFAIn,
    calculate_An_DEIn,
    calculate_An_DEInp,
    calculate_An_GutFill_BW,
    calculate_An_BWnp,
    calculate_An_GutFill_Wt,
    calculate_An_BW_empty,
    calculate_An_REgain_Calf,
    calculate_An_MEIn,
    calculate_An_NEIn,
    calculate_An_NE,
    calculate_An_MBW,
    calculate_An_data_initial,
    calculate_An_data_complete,
    calculate_An_MPIn,
    calculate_An_MPIn_g
)

from nasem_dairy.NASEM_equations.dev_gestation_equations import (
    calculate_Uter_Wtpart,
    calculate_Uter_Wt,
    calculate_GrUter_Wtpart,
    calculate_GrUter_Wt,
    calculate_Uter_BWgain,
    calculate_GrUter_BWgain,
    calculate_Gest_NCPgain_g,
    calculate_Gest_NPgain_g,
    calculate_Gest_NPuse_g,
    calculate_Gest_CPuse_g
)

from nasem_dairy.NASEM_equations.dev_fecal_equations import (
    calculate_Fe_rOMend,
    calculate_Fe_RUP,
    calculate_Fe_RumMiCP,
    calculate_Fe_CPend_g,
    calculate_Fe_CPend,
    calculate_Fe_CP
)



from nasem_dairy.NASEM_equations.dev_body_composition_equations import (
    calculate_CPGain_FrmGain,
    calculate_Frm_Gain,
    calculate_Frm_Gain_empty,
    calculate_NPGain_FrmGain,
    calculate_Rsrv_Gain,
    calculate_Rsrv_Gain_empty,
    calculate_Body_Gain_empty,
    calculate_Frm_NPgain,
    calculate_NPGain_RsrvGain,
    calculate_Rsrv_NPgain,
    calculate_Body_NPgain,
    calculate_Body_CPgain,
    calculate_Body_CPgain_g,
    calculate_Rsrv_Gain,
    calculate_Rsrv_Gain_empty,
    calculate_Rsrv_Fatgain,
    calculate_CPGain_FrmGain,
    calculate_Rsrv_CPgain,
    calculate_FatGain_FrmGain,
    calculate_Frm_Gain,
    calculate_Frm_Gain_empty,
    calculate_Frm_Fatgain,
    calculate_NPGain_FrmGain,
    calculate_Frm_NPgain,
    calculate_Frm_CPgain
)

from nasem_dairy.NASEM_equations.dev_urine_equations import (
    calculate_Ur_Nout_g,
    calculate_Ur_DEout
)

from nasem_dairy.NASEM_equations.dev_energy_requirement_equations import (
    calculate_An_NEmUse_NS,
    calculate_An_NEm_Act_Graze,
    calculate_An_NEm_Act_Parlor,
    calculate_An_NEm_Act_Topo,
    calculate_An_NEmUse_Act,
    calculate_An_NEmUse,
    calculate_An_MEmUse,
    calculate_Rsrv_NEgain,
    calculate_Kr_ME_RE,
    calculate_Rsrv_MEgain,
    calculate_Frm_NEgain,
    calculate_Frm_MEgain,
    calculate_An_MEgain,
    calculate_Gest_REgain,
    calculate_Gest_MEuse,
    calculate_Trg_NEmilk_Milk,
    calculate_Trg_Mlk_NEout,
    calculate_Trg_Mlk_MEout,
    calculate_Trg_MEuse
)