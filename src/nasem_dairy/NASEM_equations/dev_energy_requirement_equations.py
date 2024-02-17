import numpy as np
from nasem_dairy.ration_balancer.ration_balancer_functions import check_coeffs_in_coeff_dict

def calculate_An_NEmUse_NS(
        An_StatePhys: str, 
        An_BW: float, 
        An_BW_empty: float, 
        An_parity_rl: int, 
        Dt_DMIn_ClfLiq: float
        ) -> float:
    """
    Calculate the net energy (NE) required for maintenance (NEm) in unstressed (_NS) dairy cows, measured in megacalories per day (Mcal/d),
    taking into account the physiological state, body weight, empty body weight, parity, and dry matter intake from calf liquid diet.

    Parameters
    ----------
    An_StatePhys : str
        The physiological state of the animal ("Calf", "Heifer", "Dry Cow", "Lactating Cow", "Other").
    An_BW : float
        The body weight of the animal in kg.
    An_BW_empty : float
        The empty body weight of the animal in kg, applicable for calves.
    An_parity_rl : int
        The parity of the cow as real value from 0 to 2.
    Dt_DMIn_ClfLiq : float
        The dry matter intake from calf liquid diet in kg, applicable for calves.

    Returns
    -------
    float
        The net energy required for maintenance (NEm) in unstressed cows, in megacalories per day (mcal/d).

    Notes
    -----
    - The calculation varies based on the physiological state of the animal, with specific adjustments for calves on milk or mixed diet,
      weaned calves, heifers, and cows.
    - Reference to specific lines in the Nutrient Requirements of Dairy Cattle R Code:
        - Heifers: Line 2777
        - Calves on milk or mixed diet: Line 2779
        - Weaned calves: Line 2780
        - Cows: Line 2782
    - Based on following equations from Nutrient Requirements of Dairy Cattle book:
        - An_NEmUse_NS for cow and heifer is same as NELmaint (Mcal/d) from Equation 3-13
        - km = 0.0769 (milk and/or milk + solid) & km = 0.97 (weaned calves) from Table 10-1 (Item: NEm, kcal/kg EBW^0.75)
        - __NOTE__: these are not consistent with the values presented in Equation 20-272 ?


    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example for a calf on a milk diet
    nd.calculate_An_NEmUse_NS(
        An_StatePhys='Calf',
        An_BW=93,
        An_BW_empty=85,
        An_parity_rl=0,
        Dt_DMIn_ClfLiq=4
    )
    ```
    # """

    # Heifers, R code line 2777
    # R code note: 'Back calculated from MEm of 0.15 and Km_NE_ME = 0.66'
    An_NEmUse_NS = 0.10 * An_BW ** 0.75  
    
    # Calves drinking milk or eating mixed diet
    # R code line 2779
    if An_StatePhys == "Calf" and Dt_DMIn_ClfLiq > 0:
        An_NEmUse_NS = 0.0769 * An_BW_empty**0.75

    # Adjust NEm for weaned calves (Calf state with zero DMI from calf liquid diet)
    # R code line 2780
    elif An_StatePhys == "Calf" and Dt_DMIn_ClfLiq == 0:
        An_NEmUse_NS = 0.097 * An_BW_empty**0.75

    # Adjust NEm for cows based on parity (assuming parity > 0 implies cow)
    # R code line 2782
    elif An_parity_rl > 0:
        # This recalculates what is already set as default for Heifers
        # Equation 20-272 says An_BW is An_BW NPr_3 i.e. Equation 20-246
        An_NEmUse_NS = 0.10 * An_BW**0.75

    return An_NEmUse_NS


def calculate_An_NEm_Act_Graze(
        Dt_PastIn: float, 
        Dt_DMIn: float, 
        Dt_PastSupplIn: float, 
        An_MBW: float
        ) -> float:
    """
    Calculate the net energy (NE) used for grazing activity (NEm_Act_Graze), measured in megacalories per day (Mcal/d).
    This function estimates the additional energy expenditure due to grazing based on pasture intake, total dry matter intake, pasture supplementation,
    and the metabolic body weight of the animal.

    Parameters
    ----------
    Dt_PastIn : float
        The dry matter intake from pasture in kg/d.
    Dt_DMIn : float
        The total dry matter intake in kg/d.
    Dt_PastSupplIn : float
        The dry matter intake from supplementation in kg/d. E.g. could be supplemental concentrate or forage
    An_MBW : float
        The metabolic body weight of the animal in kg, typically calculated as the live body weight in kg to the power of 0.75.

    Returns
    -------
    float
        The net energy used for grazing activity, in megacalories per day (Mcal/d).

    Notes
    -----
    - The energy expenditure for grazing activity is considered only if the proportion of pasture intake to total dry matter intake is above a certain threshold.
    - Reference to specific line in the Nutrient Requirements of Dairy Cattle R Code:
        - Lines 2793-2795
    - Based on following equations from Nutrient Requirements of Dairy Cattle book:
        - Equation 20-274
    - This function assumes a linear decrease in energy expenditure for grazing as pasture supplementation increases, with a base value adjusted for the metabolic body weight of the animal.

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of NE used for grazing activity
    nd.calculate_An_NEm_Act_Graze(
        Dt_PastIn=15,
        Dt_DMIn=20,
        Dt_PastSupplIn=5,
        An_MBW=500
    )
    ```
    """
    if Dt_PastIn / Dt_DMIn < 0.005:     # Line 2793
        An_NEm_Act_Graze = 0
    else:
        An_NEm_Act_Graze = 0.0075 * An_MBW * (600 - 12 * Dt_PastSupplIn) / 600 # Lines 2794-5
    return An_NEm_Act_Graze


def calculate_An_NEm_Act_Parlor(
        An_BW: float, 
        Env_DistParlor: float, 
        Env_TripsParlor: float
        ) -> float:
    """
    Calculate the net energy (NE) used for activity related to walking to and from the parlor (NEm_Act_Parlor) in dairy cows,
    measured in Megacalories per day (Mcal/d). This function estimates the energy expenditure based on the distance from barn or paddock to the parlor,
    the number of daily trips to and from the parlor, and the body weight of the animal.

    Parameters
    ----------
    An_BW : float
        The body weight of the animal in kg.
    Env_DistParlor : float
        The distance from barn or paddock to the parlor in meters.
    Env_TripsParlor : float
        The number of daily trips to and from the parlor, usually two times the number of milkings.

    Returns
    -------
    float
        The net energy used for walking to the parlor activity, in Megacalories per day (Mcal/d).

    Notes
    -----
    - The energy expenditure for walking to the parlor is calculated by considering the distance, the number of trips,
      and the animal's body weight to estimate the total energy spent in this activity.
    - Reference to specific line in the Nutrient Requirements of Dairy Cattle R Code:
        - Main calculation: Line 2796
    - Based on following equations from Nutrient Requirements of Dairy Cattle book:
        - Equation 20-275

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of NE used for walking to the parlor
    nd.calculate_An_NEm_Act_Parlor(
        An_BW=650,
        Env_DistParlor=500,
        Env_TripsParlor=4
    )
    ```
    """
    An_NEm_Act_Parlor = (0.00035 * Env_DistParlor / 1000) * Env_TripsParlor * An_BW  # Line 2796
    return An_NEm_Act_Parlor


def calculate_An_NEm_Act_Topo(
        An_BW: float, 
        Env_Topo: float
        ) -> float:
    """
    Calculate the net energy (NE) used due to topographical activity (NEm_Act_Topo) in dairy cows, measured in Megacalories per day (Mcal/d).
    This function estimates the energy expenditure associated with the daily total climb due to topography and during transit between
    the milking parlor and the barn or paddock, considering only the meters of uphill climb, as downhill movement has negligible locomotion cost.

    Parameters
    ----------
    An_BW : float
        The body weight of the animal in kg.
    Env_Topo : float
        The positive elevation change per day in meters, considering only the uphill climb.

    Returns
    -------
    float
        The net energy used due to topography, in Megacalories per day (Mcal/d).

    Notes
    -----
    - The calculation takes into account the physical effort required to overcome positive elevation changes while grazing and in transit
      to and from milking, which is directly proportional to the animal's body weight and the total meters climbed uphill.
    - Reference to Equation 20-276 in the Nutrient Requirements of Dairy Cattle book and specific line in the R Code:
        - Main calculation: Line 2797

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of NE used due to topographical activity
    nd.calculate_An_NEm_Act_Topo(
        An_BW=650,
        Env_Topo=100  # Assuming 100 meters of uphill climb per day
    )
    ```
    """
    An_NEm_Act_Topo = 0.0067 * Env_Topo / 1000 * An_BW     # Line 2797
    return An_NEm_Act_Topo


def calculate_An_NEmUse_Act(An_NEm_Act_Graze: float, An_NEm_Act_Parlor: float, An_NEm_Act_Topo: float) -> float:
    """
    Calculate the total net energy (NE) used for activity (An_NEmUse_Act) in dairy cows, measured in Megacalories per day (Mcal/d).
    This function sums the energy expenditures due to grazing, walking to and from the parlor, and navigating topography.

    Parameters
    ----------
    An_NEm_Act_Graze : float
        The net energy used for grazing activity, in Mcal/d.
    An_NEm_Act_Parlor : float
        The net energy used for walking to and from the parlor, in Mcal/d.
    An_NEm_Act_Topo : float
        The net energy used due to topography (positive elevation change), in Mcal/d.

    Returns
    -------
    float
        The total net energy used for activity, in Megacalories per day (Mcal/d).

    Notes
    -----
    - This function implements the summation of total activity costs as per Equation 20-277 from the Nutrient Requirements of Dairy Cattle book.
    - Reference to specific line in the Nutrient Requirements of Dairy Cattle R Code:
        - Main calculation: Line 2798

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of total NE used for activity
    nd.calculate_An_NEmUse_Act(
        An_NEm_Act_Graze=3.3,
        An_NEm_Act_Parlor=0.5,
        An_NEm_Act_Topo=0.4
    )
    ```
    """
    An_NEmUse_Act = An_NEm_Act_Graze + An_NEm_Act_Parlor + An_NEm_Act_Topo  # Line 2798
    return An_NEmUse_Act


def calculate_An_NEmUse(An_NEmUse_NS: float, An_NEmUse_Act: float, coeff_dict: dict) -> float:
    """
    Calculate the total net energy (NE) used for maintenance (NEmUse) in dairy cows, measured in Megacalories per day (Mcal/d).
    This function computes the sum of net energy for non-stressed maintenance, net energy used for activities, and net energy used due to environmental factors.

    Parameters
    ----------
    An_NEmUse_NS : float
        The net energy used for non-stressed maintenance, in Mcal/d.
    An_NEmUse_Act : float
        The total net energy used for activity, in Mcal/d.
    coeff_dict : dict
        A dictionary containing coefficients required for the calculation, specifically 'An_NEmUse_Env' for environmental energy use.

    Returns
    -------
    float
        The total net energy used for maintenance, in Megacalories per day (Mcal/d).

    Notes
    -----
    - This function calculates the adjusted net energy for maintenance (NEm) as per Equation 20-278 from the Nutrient Requirements of Dairy Cattle book.
    - Requires the coefficient for environmental net energy use ('An_NEmUse_Env') within the coeff_dict
    - Reference to specific line in the Nutrient Requirements of Dairy Cattle R Code:
        - Main calculation: Line 2802

    - TODO: The An_NEmUse_Env should be 0 unless otherwise calculated, lines 2786-2790. Consider removing from coeff_dict.

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of total NE used for maintenance
    example_coeff_dict = {'An_NEmUse_Env': 0.05}
    nd.calculate_An_NEmUse(
        An_NEmUse_NS=1.2,
        An_NEmUse_Act=0.35,
        coeff_dict=example_coeff_dict
    )
    ```
    """
    req_coeff = ['An_NEmUse_Env']
    check_coeffs_in_coeff_dict(coeff_dict, req_coeff)
    An_NEmUse = An_NEmUse_NS + coeff_dict['An_NEmUse_Env'] + An_NEmUse_Act  # Line 2802
    return An_NEmUse


def calculate_An_MEmUse(
        An_NEmUse: float, 
        coeff_dict: dict) -> float:
    """
    Calculate the total Metabolizable Energy (MEm) used for maintenance in dairy cows, measured in Megacalories per day (Mcal/d).
    This function converts net energy (NEm) use for maintenance into metabolizable energy (MEm) use by applying a conversion efficiency coefficient (Km_ME_NE),
    which varies based on physiological state and specific feeding conditions.

    Parameters
    ----------
    An_NEmUse : float
        The total net energy used for maintenance, in Mcal/d.
    coeff_dict : dict
        A dictionary containing the conversion coefficient 'Km_ME_NE' for converting NEm to MEm.

    Returns
    -------
    float
        The total metabolizable energy used for maintenance, in Megacalories per day (Mcal/d).

    Notes
    -----
    - The conversion coefficient 'Km_ME_NE' is crucial for calculating MEm from NEm and must be determined based on the animal's physiological state
      and specific feeding conditions, such as dry feed only, liquid feed only, or mixed feeding for calves, and standard values for heifers,
      lactating cows, or dry cows.
    - Reference to specific line in the Nutrient Requirements of Dairy Cattle R Code:
        - Main calculation: Line 2845
    - See equations 20-279 to 20-282

    - TODO: Remove coeff_dict and replace with further functions, Include refactored code below for the original lines 2806-2818 in R Code.
    - NOTE: The value used for liquid feed in R is 0.723 but in book it is 0.718 (equation 20-280)

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of total MEm used for maintenance
    coeff_dict = {'Km_ME_NE': 0.66}  # Example coefficient for a lactating cow
    nd.calculate_An_MEmUse(
        An_NEmUse=2.5,
        coeff_dict=coeff_dict
    )
    ```
    """
    req_coeff = ['Km_ME_NE']
    check_coeffs_in_coeff_dict(coeff_dict, req_coeff)
    # Km_ME_NE is based on further inputs. The following is refactored version of lines 2806-2818
    # # Calculate dry matter intake from dry feed and corresponding ME and NE values for calves
    # An_MEIn_ClfDry = An_MEIn - Dt_MEIn_ClfLiq
    # An_ME_ClfDry = An_MEIn_ClfDry / (An_DMIn - Dt_DMIn_ClfLiq) if (An_DMIn - Dt_DMIn_ClfLiq) > 0 else 0
    # An_NE_ClfDry = 1.1104 * An_ME_ClfDry - 0.0946 * An_ME_ClfDry**2 + 0.0065 * An_ME_ClfDry**3 - 0.7783

    # # Initialize Km_ME_NE with a default value or None to handle unexpected physiological states
    # Km_ME_NE = None

    # # Set Km_ME_NE based on physiological state and specific conditions
    # if An_StatePhys == "Calf":
    #     if Dt_DMIn_ClfLiq == 0 and An_ME_ClfDry > 0 and An_NE_ClfDry > 0:
    #         # Dry feed only
    #         Km_ME_NE = An_NE_ClfDry / An_ME_ClfDry
    #     elif Dt_DMIn_ClfStrt == 0 and Dt_DMIn_ClfLiq > 0:
    #         # Liquid feed only
    #         Km_ME_NE = 0.723
    #     else:
    #         # Default to mixed dry and liquid feed for calves
    #         Km_ME_NE = 0.69
    # elif An_StatePhys == "Heifer":
    #     Km_ME_NE = 0.63
    # elif An_StatePhys == "Lactating Cow" or An_StatePhys == "Dry Cow":
    #     Km_ME_NE = 0.66

    An_MEmUse = An_NEmUse / coeff_dict['Km_ME_NE']      # Line 2845
    return An_MEmUse


def calculate_Rsrv_NEgain(
        Rsrv_Fatgain: float, 
        Rsrv_CPgain: float
        ) -> float:
    """
    Calculate the net energy (NE) of body reserve gain in dairy cows, measured in Megacalories per day (Mcal/d).
    This function estimates the energy content of body reserve gains based on the relative proportions of fat and protein gained,
    using their respective heats of combustion.

    Parameters
    ----------
    Rsrv_Fatgain : float
        The amount of body fat gained in kg/day.
    Rsrv_CPgain : float
        The amount of crude protein (CP) gained in kg/day.

    Returns
    -------
    float
        The net energy of body reserve gain, in Megacalories per day (Mcal/d).

    Notes
    -----
    - The energy value of a kilogram of true body tissue that is lost or gained is dependent on the relative proportions of fat and protein in the tissue and their respective heat of combustion.
    - The committee, as in the seventh edition of the Nutrient Requirements of Dairy Cattle, chose 9.4 Mcal/kg for retained body fat and 5.55 Mcal/kg for retained body protein as the heats of combustion.
    - This calculation is based on Equation 3-20c from the Nutrient Requirements of Dairy Cattle book.
    
    - NOTE: Comment in original R code: "These are really REgain.  Abbreviations on NEgain need to be sorted out. MDH"

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of NE of body reserve gain
    nd.calculate_Rsrv_NEgain(
        Rsrv_Fatgain=0.2,  # 0.2 kg of body fat gained per day
        Rsrv_CPgain=0.05   # 0.05 kg of crude protein gained per day
    )
    ```
    """
    Rsrv_NEgain = 9.4 * Rsrv_Fatgain + 5.55 * Rsrv_CPgain              # Line 2867 #These are really REgain.  Abbreviations on NEgain need to be sorted out. MDH
    return Rsrv_NEgain


def calculate_Kr_ME_RE(Trg_MilkProd: float, Trg_RsrvGain: float) -> float:
    """
    Select the efficiency of metabolizable energy (ME) conversion to retained energy (RE). The efficiency varies based on the physiological state and whether
    the animal is gaining or losing body reserves.

    Parameters
    ----------
    Trg_MilkProd : float
        The targeted milk production in kg/day. A value greater than 0 indicates a lactating cow.
    Trg_RsrvGain : float
        The targeted body reserve gain in kg/day. Positive values indicate gain, while negative values indicate loss.

    Returns
    -------
    float
        The efficiency of ME to RE conversion for reserves gain or loss, varying by physiological state.

    Notes
    -----
    - This function categorizes animals into three scenarios based on their milk production and reserve gain targets:
        1. Lactating cows with positive reserve gain have an efficiency of 0.75.
        2. Animals (typically cows) losing reserves have an efficiency of 0.89, reflecting the higher efficiency when metabolizing reserves for energy.
        3. Heifers and dry cows gaining reserves, or lactating cows without specified milk production but with reserve gain, have an efficiency of 0.60.

    - Reference to specific line in the Nutrient Requirements of Dairy Cattle R Code:
        - Lines 2835-7
    - Values from book appear to be from Table 3-2.
        - Text on Page 34 (above equation 3-19a) & Table 3-2 mentions a Kr_ME_RE of 0.74 for lactating cows (but 0.75 is used in model)
        - Dry cow: 0.60 is consistent between model and Table 3-2
        - 0.89 appears to be the conversion of RE to NEL, i.e. because gain is negative the RE is being converted to NEL

    
    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation for a lactating cow gaining reserves
    nd.calculate_Kr_ME_RE(
        Trg_MilkProd=20,  # 20 kg of milk production per day
        Trg_RsrvGain=0.2  # 0.2 kg of body reserve gain per day
    )
    ```

    """
    if Trg_MilkProd > 0 and Trg_RsrvGain > 0:   # Efficiency of ME to Rsrv RE for lactating cows gaining Rsrv, Line 2836
        Kr_ME_RE = 0.75
    elif Trg_RsrvGain <= 0:     # Line 2837, Efficiency of ME generated for cows losing Rsrv
        Kr_ME_RE = 0.89
    else:
        # Efficiency of ME to RE for reserves gain, Heifers and dry cows, Line 2835
        Kr_ME_RE = 0.60
    return Kr_ME_RE


def calculate_Rsrv_MEgain(Rsrv_NEgain: float, Kr_ME_RE: float) -> float:
    """
    Calculate the metabolizable energy (ME) of body reserve gain in dairy cows, measured in Megacalories per day (Mcal/d).
    This function uses the net energy (NE) gain from body reserves and the efficiency of ME conversion to reserve energy (RE) to
    estimate the total ME associated with body reserve gains.

    Parameters
    ----------
    Rsrv_NEgain : float
        The net energy of body reserve gain, in Mcal/d. 
    Kr_ME_RE : float
        The efficiency of metabolizable energy to reserve energy conversion for reserves gain. 

    Returns
    -------
    float
        The metabolizable energy associated with body reserve gain, in Megacalories per day (Mcal/d).

    Notes
    -----
    - The calculation inversely applies the conversion efficiency (Kr_ME_RE) to the net energy gain (Rsrv_NEgain) to estimate the metabolizable
      energy required for the observed gain in body reserves.
    - Reference to line number in the Nutrient Requirements of Dairy Cattle R Code: Line 2872

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of ME associated with body reserve gain
    nd.calculate_Rsrv_MEgain(
        Rsrv_NEgain=1.5,  # 1.5 Mcal/d of net energy gain from body reserves
        Kr_ME_RE=0.75     # Efficiency of ME to RE conversion for reserves gain
    )
    ```
    """
    Rsrv_MEgain = Rsrv_NEgain / Kr_ME_RE    # Line 2872
    return Rsrv_MEgain


def calculate_Frm_NEgain(Frm_Fatgain: float, Frm_CPgain: float) -> float:
    """
    Calculate the net energy (NE) of frame gain in dairy cows, measured in Megacalories per day (Mcal/d).
    This function estimates the energy content of frame gains based on the amounts of fat and protein gained,
    utilizing their respective heats of combustion.

    Parameters
    ----------
    Frm_Fatgain : float
        The amount of fat gained in the frame, in kg/d. Normally calculated by [](`~nasem_dairy.NASEM_equations.dev_body_composition_equations.calculate_Frm_Fatgain`).
    Frm_CPgain : float
        The amount of crude protein (CP) gained in the frame, in kg/d. Normally calculated by [](`~nasem_dairy.NASEM_equations.dev_body_composition_equations.calculate_Frm_CPgain`).

    Returns
    -------
    float
        The retained energy of frame gain, in Megacalories per kg.

    Notes
    -----
    - The energy value of frame tissue gain is calculated similarly to body reserve gains, based on the relative proportions of fat and protein in the tissue and their respective heat of combustion.
    - The committee, as in the seventh edition of the Nutrient Requirements of Dairy Cattle, chose 9.4 Mcal/kg for fat and 5.55 Mcal/kg for protein as the heats of combustion for these components (page 257)
    - This calculation is based on following equations from the Nutrient Requirements of Dairy Cattle book:
       - Equation 11-5d (RE_EBG) - However, this version takes Frm_Fatgain and Frm_CPgain which are kg/d (based on target frame gain input) whereas the book calculates per kg of gain, i.e. with Fat_EBG (kg/kg) and Protein_EBG (kg/kg)
       - Note that Equation 3-20c (RE_FADG; frame average daily gain) is similar, but is correcting for empty body weight in 3-20a and 2-20b via (EBG/ADG) which is empty body weight gain / live BW gain, which is 0.85 for 15% assumption.
    - Reference to specific line in the Nutrient Requirements of Dairy Cattle R Code: Line 2867.

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of NE of frame gain
    nd.calculate_Frm_NEgain(
        Frm_Fatgain=0.1,  # 0.1 kg of fat gained in the frame per day
        Frm_CPgain=0.05   # 0.05 kg of crude protein gained in the frame per day
    )
    ```
    """
    Frm_NEgain = 9.4 * Frm_Fatgain + 5.55 * Frm_CPgain      # Line 2867
    return Frm_NEgain 


def calculate_Frm_MEgain(Frm_NEgain: float, coeff_dict: dict) -> float:
    """
    Calculate the metabolizable energy (ME) of frame gain in dairy cows, measured in Megacalories per day (Mcal/d).
    This function converts retained energy (RE) gain from frame tissue into metabolizable energy (ME) using a conversion coefficient (Kf_ME_RE).

    Parameters
    ----------
    Frm_NEgain : float
        The net energy gain from frame tissue (should be called retained energy), in Mcal/d. Normally calculated by [](`~nasem_dairy.NASEM_equations.dev_energy_requirement_equations.calculate_Frm_NEgain`)
    coeff_dict : dict
        A dictionary containing the conversion coefficient 'Kf_ME_RE' for converting RE to ME for frame gains.

    Returns
    -------
    float
        The metabolizable energy associated with frame gain, in Megacalories per day (Mcal/d).

    Notes
    -----
    - The conversion coefficient 'Kf_ME_RE' is currently specified in the coeff_dict. 
    - TODO: However, update code with logic for selecting correct Kf_ME_RE - might still need to have defaults set in coeff_dict for calf liquid (0.56) and cow/heifer (0.4)

    - Reference to specific line in the Nutrient Requirements of Dairy Cattle R Code: Line 2873.
    - This calculation is based on following equations from the Nutrient Requirements of Dairy Cattle book:
        - Equation 3-20d - noting that here `Frm_NEgain` should really be called RE (retained energy), and that 0.4 in book is default value for Kf_ME_RE

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of ME associated with frame gain
    coeff_dict = {'Kf_ME_RE': 0.4}  # Example conversion coefficient for frame gain
    nd.calculate_Frm_MEgain(
        Frm_NEgain=1.0,  # 1.0 Mcal/d of net energy gain from frame tissue
        coeff_dict=coeff_dict
    )
    ```
    """
    req_coeff = ['Kf_ME_RE']
    check_coeffs_in_coeff_dict(coeff_dict, req_coeff)
    # Lines 2827 - 2832
    # ## Frame (f) Gain (excludes Reserves Gain or Loss) ##
    # #Calf frame gain
    # Kf_ME_RE_ClfLiq <- 0.56
    # Kf_ME_RE_ClfDry <- (1.1376*An_DE*0.93 -0.1198*(An_DE*0.93)^2+0.0076*(An_DE*0.93)^3-1.2979)/(An_DE*0.93)
    # Kf_ME_RE_Clf <- Kf_ME_RE_ClfLiq*Dt_DMIn_ClfLiq/Dt_DMIn + Kf_ME_RE_ClfDry*(Dt_DMIn-Dt_DMIn_ClfLiq)/Dt_DMIn

    # Kf_ME_RE <- ifelse(An_StatePhys == "Calf", Kf_ME_RE_Clf, 0.4)    #Default frame gain is 0.4 for heifers and cows
    
    Frm_MEgain = Frm_NEgain / coeff_dict['Kf_ME_RE'] # Line 2873
    return Frm_MEgain


def calculate_An_MEgain(Rsrv_MEgain: float, Frm_MEgain: float) -> float:
    """
    *Calculate Animal (An) Metabolizable Energy (ME) Gain*

    Calculate the total ME required for both frame and reserve gain in the animal, measured in Megacalories per day (Mcal/d).

    Parameters
    ----------
    Rsrv_MEgain : float
        The metabolizable energy of body reserve gain, in Mcal/d. Normally calculated by 
        [](`~nasem_dairy.NASEM_equations.dev_energy_requirement_equations.calculate_Rsrv_MEgain`).
    Frm_MEgain : float
        The metabolizable energy of frame gain, in Mcal/d. Normally calculated by 
        [](`~nasem_dairy.NASEM_equations.dev_energy_requirement_equations.calculate_Frm_MEgain`).

    Returns
    -------
    float
        The total metabolizable energy required for frame and reserve gain, in Mcal/d.

    Notes
    -----
    - Reference to specific line in the Nutrient Requirements of Dairy Cattle R Code: Line 2874.
    - Equation from the Nutrient Requirements of Dairy Cattle book: Equation 20-247

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of total ME required for frame and reserve gain
    nd.calculate_An_MEgain(
        Rsrv_MEgain=1.5,  # Metabolizable energy gain from body reserves, in Mcal/d
        Frm_MEgain=0.5    # Metabolizable energy gain from frame, in Mcal/d
    )
    ```
    """
    An_MEgain = Rsrv_MEgain + Frm_MEgain    # Line 2874
    return An_MEgain


def calculate_Gest_REgain(GrUter_BWgain: float, coeff_dict: dict) -> float:
    """
    *Calculate Gestation (Gest) Retained Energy (RE) Gain*

    Calculate the gestational requirements for net energy (NE, Mcal/d) based on the change in gravid uterus weight during gestation (GrUter_BWgain; kg/d) 
    multiplied by the concentration of energy in the final gravid uterus at parturition (NE_GrUtWt, Mcal/kg)
    

    Parameters
    ----------
    GrUter_BWgain : float
        The gross uterine body weight gain (or loss) in kg/d, representing changes due to uterine growth or regression. Usually calculated by [](`~nasem_dairy.NASEM_equations.dev_gestation_equations.calculate_GrUter_BWgain`)
    coeff_dict : dict
        A dictionary containing the coefficient 'NE_GrUtWt' which is the concentration of NE per kg of fresh Gravid Uterus weight at birth (Mcal/kg), defaults to 0.95.

    Returns
    -------
    float
        The RE gain for gestation (called NE in book), accounting for uterine growth or regression, in Mcal/d.

    Notes
    -----
    - While this method estimates the release or requirement of NE for uterine weight changes, a note was left in the R code that says it will slightly underestimates the release of NE from the regressing uterus.
    - Reference to specific line in the Nutrient Requirements of Dairy Cattle R Code: Line 2361.
    - Equation from the Nutrient Requirements of Dairy Cattle book: Equation 20-234 & Table 20-10

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of gestation RE gain
    coeff_dict = {'NE_GrUtWt': 0.95}  
    nd.calculate_Gest_REgain(
        GrUter_BWgain=0.1,  # 0.1 kg/d of uterine body weight gain
        coeff_dict=coeff_dict
    )
    ```
    """
    Gest_REgain = GrUter_BWgain * coeff_dict['NE_GrUtWt']   # This will slightly underestimate release of NE from the regressing uterus, Line 2361
    return Gest_REgain


def calculate_Gest_MEuse(Gest_REgain: float) -> float:
    """
    *Calculate Gestation (Gest) Metabolizable Energy (ME) Use*

    Calculate the ME requirement for gestation in dairy cows, measured in Megacalories per day (Mcal/d).
    This function determines the ME needed to support gestation, taking into account the reserve energy (RE) gain for gestation and adjusting for energy efficiencies.

    Parameters
    ----------
    Gest_REgain : float
        The reserve energy gain for gestation, in Mcal/d. Normally calculated by 
        [](`~nasem_dairy.NASEM_equations.dev_energy_requirement_equations.calculate_Gest_REgain`).

    Returns
    -------
    float
        The ME requirement for gestation, in Mcal/d.

    Notes
    -----
    - The efficiency of energy use (Ky_ME_NE), expressed in Mcal NE/Mcal ME, varies based on whether there is a gain (0.14) or loss (0.89) in gestation energy, reflecting different physiological needs during pregnancy.
    - These efficiencies are derived from Ferrell et al., 1976, with the assumption that the loss efficiency is equivalent to reserve loss efficiency.
    - This method provides insight into the additional ME required to support gestational processes, including uterine growth or regression.
    - Reference to specific line in the Nutrient Requirements of Dairy Cattle R Code: 
        - Ky_ME_NE = Line 2840
        - Gest_MEuse = Line 2860
    - Equation from the Nutrient Requirements of Dairy Cattle book:
        - Ky_ME_NE = Equation 20-236
        - Gest_MEuse = Equation 20-237

    - TODO: Consider adding the default Ky values to coeff_dict, e.g. Ky_ME_NE_gain = 0.14, Ky_ME_NE_loss = 0.89

    Examples
    --------
    ```{python}
    import nasem_dairy as nd

    # Example calculation of ME requirement for gestation
    Gest_REgain = 0.2  # 0.2 Mcal/d of RE gain for gestation
    nd.calculate_Gest_MEuse(Gest_REgain)
    ```
    """

    Ky_ME_NE = np.where(Gest_REgain >= 0, 0.14, 0.89) 
    # Gain from Ferrell et al, 1976, and loss assumed = Rsrv loss, Line 2860
    Gest_MEuse = Gest_REgain / Ky_ME_NE
    return Gest_MEuse


def calculate_Trg_NEmilk_Milk(Trg_MilkFatp: float, Trg_MilkTPp: float, Trg_MilkLacp: float) -> float:
    """
    Trg_NEmilk_Milk: Target energy output (mcal) per kg milk
    Trg = target
    p = percent
    """
    Trg_NEmilk_Milk = 9.29 * Trg_MilkFatp / 100 + 5.85 * Trg_MilkTPp / 100 + 3.95 * Trg_MilkLacp / 100  # Line 2887
    if np.isnan(Trg_NEmilk_Milk):
        # If milk protein and lactose are not provided, use the Tyrrell and Reid (1965) eqn., Line 2888
        Trg_NEmilk_Milk = 0.36 + 9.69 * Trg_MilkFatp / 100
    return Trg_NEmilk_Milk


def calculate_Trg_Mlk_NEout(Trg_MilkProd: float, Trg_NEmilk_Milk: float) -> float:
    """
    Trg_Mlk_NEout: NE requirement for milk production, mcal/d
    """
    Trg_Mlk_NEout = Trg_MilkProd * Trg_NEmilk_Milk  # Line 2889
    return Trg_Mlk_NEout


def calculate_Trg_Mlk_MEout(Trg_Mlk_NEout: float, coeff_dict: dict) -> float:
    """
    Kl_ME_NE: Conversion of NE to ME for lactation
    Trg_Mlk_MEout: ME requirement for milk production, mcal/d
    """
    req_coeff = ['Kl_ME_NE']
    check_coeffs_in_coeff_dict(coeff_dict, req_coeff)
    Trg_Mlk_MEout = Trg_Mlk_NEout / coeff_dict['Kl_ME_NE']  # Line 2890
    return Trg_Mlk_MEout


def calculate_Trg_MEuse(An_MEmUse: float, An_MEgain: float, Gest_MEuse: float, Trg_Mlk_MEout: float) -> float:
    """
    Trg_MEuse: Total metabolizable energy requirement mcal/d 
    """
    Trg_MEuse = An_MEmUse + An_MEgain + Gest_MEuse + Trg_Mlk_MEout   # Line 2923
    return Trg_MEuse


def calculate_An_MEIn_approx(An_DEInp: float, An_DENPNCPIn: float, An_DigTPaIn: float, Body_NPgain: float, An_GasEOut: float, coeff_dict: dict) -> float:
    """
    An_MEIn_approx: Approximate ME intake, see note:
        Adjust heifer MPuse target if the MP:ME ratio is below optimum for development.
        Can't calculate ME before MP, thus estimated ME in the MP:ME ratio using the target NPgain.  Will be incorrect
        if the animal is lactating or gestating.
    """
    An_MEIn_approx = An_DEInp + An_DENPNCPIn + (An_DigTPaIn - Body_NPgain) * 4.0 + Body_NPgain * coeff_dict['En_CP'] - An_GasEOut   # Line 2685
    return An_MEIn_approx
