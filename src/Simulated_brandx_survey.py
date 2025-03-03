import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------
# SET SEED FOR REPRODUCIBILITY
# -----------------------------------------------------------------------------
np.random.seed(123)

# -----------------------------------------------------------------------------
# DEMOGRAPHIC DISTRIBUTIONS (CANADIAN POPULATION PATTERNS)
# -----------------------------------------------------------------------------
def pick_gender():
    """
    A2_Gender:
    1 = Men (49%)
    2 = Women (50%)
    3 = Other (1%)
    """
    return np.random.choice([1,2,3], p=[0.49,0.50,0.01])

def pick_age():
    """
    A3_Age Groups (coded):
     1 = 18-24 (14.90%)
     2 = 25-34 (19.55%)
     3 = 35-44 (18.15%)
     4 = 45-54 (15.78%)
     5 = 55-64 (15.99%)
     6 = 65+   (15.63%)
    """
    age_probs = [0.1490, 0.1955, 0.1815, 0.1578, 0.1599, 0.1563]
    age_probs = np.array(age_probs) / np.sum(age_probs)
    return np.random.choice([1,2,3,4,5,6], p=age_probs)

# Province mapping with realistic Canadian distribution
PROVINCE_MAPPING = {
    1:"Alberta",
    2:"British Columbia",
    3:"Manitoba",
    4:"New Brunswick",
    5:"Newfoundland and Labrador",
    6:"Northwest Territories",
    7:"Nova Scotia",
    8:"Nunavut",
    9:"Ontario",
    10:"Prince Edward Island",
    11:"Quebec",
    12:"Saskatchewan",
    13:"Yukon"
}

def pick_province():
    """
    A4_Province with approximate percentages (source-like):
      AB=10.20109, BC=13.27141, MB=3.0633, NB=2.0422, NL=1.0211, NWT=0.515,
      NS=2.0422, NU=0.515, ON=40.3143, PE=1.0211, QC=22.45239,
      SK=3.0633, YT=0.515
    """
    prov_codes = list(PROVINCE_MAPPING.keys())
    prov_probs = np.array([
        10.20109, 13.27141, 3.0633, 2.0422, 1.0211,
        0.515, 2.0422, 0.515, 40.3143, 1.0211,
        22.45239, 3.0633, 0.515
    ])
    prov_probs = prov_probs / prov_probs.sum()
    chosen = np.random.choice(prov_codes, p=prov_probs)
    return PROVINCE_MAPPING[chosen]

def pick_community_type():
    """
    D9_Community_Type:
    1 = Urban (70%)
    2 = Suburban (20%)
    3 = Rural (10%)
    """
    return np.random.choice([1,2,3], p=[0.70,0.20,0.10])

# -----------------------------------------------------------------------------
# BRAND LIST FOR UNAIDED AWARENESS (B1) -- each ≤ 12 chars
# -----------------------------------------------------------------------------
ALL_BRANDS = [
    "Lays", "Pringles", "Ruffles", "Doritos", "Cheetos", "Smartfood", "SunChips",
    "Fritos", "Takis", "MissVickie", "KettleChip", "BrandX", "Tims", "Wise",
    "CapeCod", "PopChips", "Hawaiian", "Zapps", "Funyuns", "Krunchers",
    "Munchies", "Bugles", "Popcorners", "ChexMix", "OnionRings",
    "Herrs", "Utz", "Ranchritos", "PakiChips", "BhujaSnax"
]

# -----------------------------------------------------------------------------
# TEXT RESPONSES FOR C6 (OPEN-ENDED AD MESSAGES)
# -----------------------------------------------------------------------------
C6_RESPONSES_POSITIVE = [
    "Great taste and crunch",
    "Really enjoyed the ad and the message of fresh flavors",
    "It made me think of fun snacking moments",
    "Loved the upbeat feel and the emphasis on quality ingredients",
    "The ad was entertaining and memorable",
    "Good visuals and appealing soundtrack"
]
C6_RESPONSES_NEUTRAL_NEG = [
    "It was okay, but nothing special",
    "Not very memorable",
    "I found it somewhat boring",
    "Too repetitive for my taste"
]
C6_RESPONSES_LONGER = [
    "I really appreciated how the ad highlighted the fun aspect of snacking with friends and family. "
    "It felt relatable and encouraged me to try new flavors.",

    "The commercial showed the product in various scenarios, suggesting it's a great snack for parties, "
    "movie nights, and quick bites at home. It was quite convincing."
]

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS FOR RANDOM RESPONSE GENERATION
# -----------------------------------------------------------------------------
def simulate_completion_time(is_outlier=False):
    """
    Simulate survey completion time in minutes.
      - Normal: uniform(3,45)
      - Outlier: uniform(1,3) or uniform(45,60)
    """
    if is_outlier:
        if np.random.rand() < 0.5:
            return round(np.random.uniform(1,3),1)
        else:
            return round(np.random.uniform(45,60),1)
    else:
        return round(np.random.uniform(3,45),1)

def simulate_snack_response(avoid_all_never=False):
    """
    A6 Snack consumption scale:
      1 = Daily
      2 = 2-3 times/week
      3 = Few times/month
      4 = Rarely
      5 = Never
    If avoid_all_never=True, the probability of 'Never'=0 for that single item.
    """
    probs = np.array([0.15, 0.25, 0.30, 0.20, 0.10])
    if avoid_all_never:
        probs[-1] = 0.0
        probs /= probs.sum()
    return np.random.choice([1,2,3,4,5], p=probs)

def simulate_b1_unaided_brands(is_exposed=False, frequent_chip_eater=False):
    """
    B1: Up to 3 brand mentions from the brand list (≤12 chars each).
    - If is_exposed => higher chance to include 'BrandX'
    - If frequent_chip_eater => higher chance to include top chip brands
    """
    num_brands = np.random.choice([1,2,3], p=[0.4,0.4,0.2])
    chosen = []

    # Increase chance BrandX if is_exposed
    if is_exposed and np.random.rand()<0.60:
        chosen.append("BrandX")

    # Weighted approach for frequent chip eaters
    popular_brands = ["Lays","Pringles","Ruffles","Doritos","Cheetos","BrandX"]
    needed = num_brands - len(chosen)
    if needed<0:
        needed=0

    for _ in range(needed):
        if frequent_chip_eater and np.random.rand()<0.50:
            chosen.append(np.random.choice(popular_brands))
        else:
            chosen.append(np.random.choice(ALL_BRANDS))

    # Remove duplicates if any, but keep the count to num_brands
    chosen = list(set(chosen))
    while len(chosen)<num_brands:
        chosen.append(np.random.choice(ALL_BRANDS))

    np.random.shuffle(chosen)
    return ", ".join(chosen[:num_brands])

def simulate_aided_awareness():
    """
    B2: Aided brand awareness from among:
      1=BrandX, 2=Lays, 3=Pringles, 4=Ruffles, 5=Utz, 6=Kettle Brand, 7=Herr's, 8=Other
    Typically pick 2–4.
    Returns a string like "1, 3, 5".
    """
    options = [1,2,3,4,5,6,7]
    num_selected = np.random.choice([2,3,4], p=[0.3,0.5,0.2])
    sel = list(np.random.choice(options, size=num_selected, replace=False))
    if np.random.rand()<0.1:
        sel.append(8)  # "Other"
    sel.sort()
    return ", ".join(map(str, sel))

def simulate_overall_impression(aided_str):
    """
    B2a: For each brand selected in B2, generate a 1–10 slider rating.
    E.g. "Brand X:8, Lay's:7"
    """
    mapping = {
        1:"Brand X", 2:"Lay's", 3:"Pringles", 4:"Ruffles",
        5:"Utz", 6:"Kettle Brand", 7:"Herr's", 8:"Other"
    }
    if not aided_str:
        return ""
    codes = [int(x.strip()) for x in aided_str.split(",")]
    results=[]
    for c in codes:
        r = int(np.round(np.random.uniform(1,10)))
        results.append(f"{mapping[c]}:{r}")
    return ", ".join(results)

def simulate_attitude():
    """
    Returns a 1–5 Likert with mild positive skew:
      5=40%, 4=35%, 3=10%, 2=10%, 1=5%
    Used for C5 (Ad attitudes) or other agreement scales.
    """
    return np.random.choice([1,2,3,4,5], p=[0.05,0.10,0.10,0.35,0.40])

# -----------------------------------------------------------------------------
# CORRELATED BRAND X RATINGS (B3, B4, B5)
# -----------------------------------------------------------------------------
def adjust_brandx_ratings(b3, b4, b5, brandx_in_b1=False, is_exposed=False):
    """
    B3 & B4 in 1..5 scale, B5 in 1..10 scale.
    Nudges them so:
      - B4 >= B3 (logical correlation)
      - If brandx_in_b1 => push them up a bit
      - If is_exposed => also push them up
      - B5 is correlated with B4 (if B4 is 5 => B5 ~8..10)
    """
    # Ensure B4 >= B3
    if b4 < b3:
        b4 = b3

    # If brandX mentioned => small bump
    if brandx_in_b1:
        if b3 < 5: b3 += 1
        if b4 < 5: b4 += 1

    # If exposed => random bump
    if is_exposed:
        if b3 < 5 and np.random.rand()<0.5:
            b3 += 1
        if b4 < 5 and np.random.rand()<0.5:
            b4 += 1

    # Re-check
    if b4 < b3:
        b4 = b3

    # B5 ~ around a center for each B4
    center_map = {1:2, 2:4, 3:6, 4:8, 5:9}
    center = center_map[b4]
    if is_exposed:
        center += 0.5
    val = np.clip(np.random.normal(loc=center, scale=1.0), 1, 10)
    new_b5 = int(round((b5 + val)/2.0))  # average old b5 with the new random
    new_b5 = max(1, min(10, new_b5))

    return b3, b4, new_b5

# -----------------------------------------------------------------------------
# SECTION C (Ad Perceptions) CORRELATIONS:
#  - If Exposed, fill out. If not, everything = NaN.
#  - Higher channel frequency => more likely recall.
#  - Higher recall => typically higher enjoyment & more positive attitude
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# TERMINATION SIMULATION
# -----------------------------------------------------------------------------
def simulate_terminated_respondent(resp_id):
    """
    Creates a partially complete / terminated record with one of three scenarios:
      1) A1 Termination (didn't purchase snack => everything else NaN)
      2) A6 Termination (all 'Never' => end)
      3) MidSurvey Termination (some B but no C or D)
    We do NOT force channels for terminated (they do not count towards the final 500/500 distribution).
    """
    termination_types = ["A1","A6","MidSurvey"]
    tp = np.random.choice(termination_types, p=[0.3,0.4,0.3])

    if tp=="A1":
        # Fail at screening => A1 not 1 => everything else is NaN
        return {
            "respondent_id": resp_id,
            "Completed": 0,
            "Termination_Point": "A1",
            "A1_purchased_snack": np.random.choice([2,99]),
            "A2_gender": np.nan,
            "A3_age": np.nan,
            "A4_province": np.nan,
            "TV_Channel_A": np.nan,
            "TV_Channel_B": np.nan,
            "TV_Channel_C": np.nan,
            "TV_Channel_D": np.nan,
            "TV_Channel_E": np.nan,
            "A6_PotatoChips": np.nan,
            "A6_Popcorn": np.nan,
            "A6_Pretzels": np.nan,
            "A6_Chocolate": np.nan,
            "A6_GranolaBars": np.nan,
            "A6_FruitSlices": np.nan,
            "Exposed_Flag": np.nan,
            "B1_Unaided_BrandAwareness": np.nan,
            "B2_Aided_BrandAwareness": np.nan,
            "B2a_Overall_Impression": np.nan,
            "B3_Familiarity_BrandX": np.nan,
            "B4_Consideration_BrandX": np.nan,
            "B5_Recommendation_BrandX": np.nan,
            "C1_Ad_Recall_Pre": np.nan,
            "C2_Ad_Source": np.nan,
            "C3_Ad_Recall_Post": np.nan,
            "C4_Ad_Enjoyment": np.nan,
            "C5_Ad_Attitudes": np.nan,
            "C6_Key_Message_Unaided": np.nan,
            "C7_Key_Message_Aided": np.nan,
            "D1_Grocery_Shopper_Role": np.nan,
            "D2_Snack_Purchase_Frequency": np.nan,
            "D3_Weekly_Snack_Spend": np.nan,
            "D4_Employment_Status": np.nan,
            "D5_Education_Level": np.nan,
            "D6_Marital_Status": np.nan,
            "D7_Children": np.nan,
            "D8_Children_Age": np.nan,
            "D9_Community_Type": np.nan,
            "D10_Household_Income": np.nan,
            "Completion_Time": simulate_completion_time(False)
        }

    elif tp=="A6":
        # A1=1 => but then A6 => all 'Never' => termination
        return {
            "respondent_id": resp_id,
            "Completed": 0,
            "Termination_Point": "A6",
            "A1_purchased_snack": 1,
            "A2_gender": pick_gender(),
            "A3_age": pick_age(),
            "A4_province": pick_province(),
            "TV_Channel_A": np.random.choice([1,2,3,4,5]),
            "TV_Channel_B": np.random.choice([1,2,3,4,5]),
            "TV_Channel_C": np.random.choice([1,2,3,4,5]),
            "TV_Channel_D": np.random.choice([1,2,3,4,5]),
            "TV_Channel_E": np.random.choice([1,2,3,4,5]),
            "A6_PotatoChips":5,
            "A6_Popcorn":5,
            "A6_Pretzels":5,
            "A6_Chocolate":5,
            "A6_GranolaBars":5,
            "A6_FruitSlices":5,
            # We randomize Exposed_Flag but they don't actually continue
            "Exposed_Flag": np.random.choice([0,1]),
            "B1_Unaided_BrandAwareness": np.nan,
            "B2_Aided_BrandAwareness": np.nan,
            "B2a_Overall_Impression": np.nan,
            "B3_Familiarity_BrandX": np.nan,
            "B4_Consideration_BrandX": np.nan,
            "B5_Recommendation_BrandX": np.nan,
            "C1_Ad_Recall_Pre": np.nan,
            "C2_Ad_Source": np.nan,
            "C3_Ad_Recall_Post": np.nan,
            "C4_Ad_Enjoyment": np.nan,
            "C5_Ad_Attitudes": np.nan,
            "C6_Key_Message_Unaided": np.nan,
            "C7_Key_Message_Aided": np.nan,
            "D1_Grocery_Shopper_Role": np.nan,
            "D2_Snack_Purchase_Frequency": np.nan,
            "D3_Weekly_Snack_Spend": np.nan,
            "D4_Employment_Status": np.nan,
            "D5_Education_Level": np.nan,
            "D6_Marital_Status": np.nan,
            "D7_Children": np.nan,
            "D8_Children_Age": np.nan,
            "D9_Community_Type": np.nan,
            "D10_Household_Income": np.nan,
            "Completion_Time": simulate_completion_time(False)
        }

    else:  # MidSurvey
        # partial brand metrics in B, no C or D
        A2 = pick_gender()
        A3 = pick_age()
        A4 = pick_province()

        # A6 => not all never
        snack_items = [simulate_snack_response(True) for _ in range(6)]
        B1 = simulate_b1_unaided_brands(is_exposed=False, frequent_chip_eater=(snack_items[0] in [1,2]))
        B2 = simulate_aided_awareness()
        B2a = simulate_overall_impression(B2)
        B3 = np.random.choice([1,2,3,4,5], p=[0.05,0.15,0.20,0.35,0.25])
        B4 = np.random.choice([1,2,3,4,5], p=[0.05,0.15,0.20,0.35,0.25])
        B5 = int(np.clip(np.random.normal(6,1.8),1,10))
        # Adjust for correlation
        B3, B4, B5 = adjust_brandx_ratings(
            b3=B3, b4=B4, b5=B5,
            brandx_in_b1=("BrandX" in B1),
            is_exposed=False
        )

        return {
            "respondent_id": resp_id,
            "Completed": 0,
            "Termination_Point": "MidSurvey",
            "A1_purchased_snack": 1,
            "A2_gender": A2,
            "A3_age": A3,
            "A4_province": A4,
            "TV_Channel_A": np.random.choice([1,2,3,4,5]),
            "TV_Channel_B": np.random.choice([1,2,3,4,5]),
            "TV_Channel_C": np.random.choice([1,2,3,4,5]),
            "TV_Channel_D": np.random.choice([1,2,3,4,5]),
            "TV_Channel_E": np.random.choice([1,2,3,4,5]),
            "A6_PotatoChips": snack_items[0],
            "A6_Popcorn": snack_items[1],
            "A6_Pretzels": snack_items[2],
            "A6_Chocolate": snack_items[3],
            "A6_GranolaBars": snack_items[4],
            "A6_FruitSlices": snack_items[5],
            "Exposed_Flag": np.random.choice([0,1]),
            "B1_Unaided_BrandAwareness": B1,
            "B2_Aided_BrandAwareness": B2,
            "B2a_Overall_Impression": B2a,
            "B3_Familiarity_BrandX": B3,
            "B4_Consideration_BrandX": B4,
            "B5_Recommendation_BrandX": B5,
            "C1_Ad_Recall_Pre": np.nan,
            "C2_Ad_Source": np.nan,
            "C3_Ad_Recall_Post": np.nan,
            "C4_Ad_Enjoyment": np.nan,
            "C5_Ad_Attitudes": np.nan,
            "C6_Key_Message_Unaided": np.nan,
            "C7_Key_Message_Aided": np.nan,
            "D1_Grocery_Shopper_Role": np.nan,
            "D2_Snack_Purchase_Frequency": np.nan,
            "D3_Weekly_Snack_Spend": np.nan,
            "D4_Employment_Status": np.nan,
            "D5_Education_Level": np.nan,
            "D6_Marital_Status": np.nan,
            "D7_Children": np.nan,
            "D8_Children_Age": np.nan,
            "D9_Community_Type": np.nan,
            "D10_Household_Income": np.nan,
            "Completion_Time": simulate_completion_time(False)
        }

# -----------------------------------------------------------------------------
# COMPLETE RESPONDENTS, WITH NEW EXPOSED-FLAG LOGIC:
# EXPOSED GROUP = (Channel A<5 OR Channel B<5)
# CONTROL GROUP = (Channel A=5 AND Channel B=5)
#
# We'll explicitly force the channel usage for the 500 Exposed and 500 Control.
# Then we derive Exposed_Flag from those channels.
# Outliers also forced similarly but with suspicious rating patterns and times.
# -----------------------------------------------------------------------------
def simulate_complete_respondent(
    resp_id,
    force_exposed=False,
    force_control=False,
    outlier=False
):
    """
    Creates a *complete* record with the following logic:
      - If force_exposed=True => ensure (TV_Channel_A <5) OR (TV_Channel_B <5).
      - If force_control=True => ensure (TV_Channel_A=5) AND (TV_Channel_B=5).
      - We'll set the other channels (C,D,E) randomly.
      - Then we DERIVE Exposed_Flag from those channels:
           Exposed_Flag=1 if (A<5 or B<5) else 0
      - We fill out A6, B1..B5, optionally C1..C7 if Exposed_Flag=1,
        plus D1..D10. Also handle outliers (straight-line ratings, extreme times).
    """
    # Section A1 = 1 to pass screening
    A1 = 1
    A2 = pick_gender()
    A3 = pick_age()
    A4 = pick_province()

    # Force channels for group membership:
    # (We want exactly 500 forced-exposed completes and 500 forced-control completes.)
    if force_exposed:
        # ensure at least one of (A,B) is <5
        if np.random.rand()<0.5:
            TV_Channel_A = np.random.choice([1,2,3,4])  # definitely <5
            TV_Channel_B = np.random.choice([1,2,3,4,5])  # random
        else:
            TV_Channel_B = np.random.choice([1,2,3,4])
            TV_Channel_A = np.random.choice([1,2,3,4,5])
    elif force_control:
        # must have both (A,B)=5
        TV_Channel_A = 5
        TV_Channel_B = 5
    else:
        raise ValueError(
            "simulate_complete_respondent requires either force_exposed or force_control!"
        )

    # Channels C, D, E => random
    def random_tv_channel():
        return np.random.choice([1,2,3,4,5])

    TV_Channel_C = random_tv_channel()
    TV_Channel_D = random_tv_channel()
    TV_Channel_E = random_tv_channel()

    # Derive Exposed_Flag from channels:
    # if (A<5 or B<5) => Exposed=1, else 0
    if (TV_Channel_A<5) or (TV_Channel_B<5):
        derived_exposed_flag = 1
    else:
        derived_exposed_flag = 0

    # A6 => 6 snack items (make sure not all never)
    snacks = [simulate_snack_response(True) for _ in range(6)]
    if all(x==5 for x in snacks):
        # override at least one
        snacks[0] = np.random.choice([1,2,3,4])

    # B1 => brand awareness open-ended
    # We'll call them "is_exposed" if derived_exposed_flag=1 to nudge BrandX
    frequent_chip_eater = (snacks[0] in [1,2])  # daily or 2-3x/wk for potato chips
    B1 = simulate_b1_unaided_brands(
        is_exposed=(derived_exposed_flag==1),
        frequent_chip_eater=frequent_chip_eater
    )

    # B2 => aided awareness
    B2 = simulate_aided_awareness()
    B2a = simulate_overall_impression(B2)

    # Preliminary B3,B4,B5
    if outlier:
        # suspicious pattern
        B3, B4, B5 = 3,3,5
    else:
        if derived_exposed_flag==1:
            # distribution skewed more positive
            B3 = np.random.choice([1,2,3,4,5], p=[0.02,0.08,0.15,0.35,0.40])
            B4 = np.random.choice([1,2,3,4,5], p=[0.02,0.08,0.15,0.30,0.45])
            B5 = int(np.clip(np.random.normal(8,1.5),1,10))
        else:
            # balanced distribution
            B3 = np.random.choice([1,2,3,4,5], p=[0.05,0.15,0.20,0.35,0.25])
            B4 = np.random.choice([1,2,3,4,5], p=[0.05,0.15,0.20,0.35,0.25])
            B5 = int(np.clip(np.random.normal(6,1.8),1,10))

    # Correlate B3,B4,B5 with mention of BrandX in B1 & Exposed_Flag
    brandx_in_b1 = ("BrandX" in B1.split(", "))
    B3, B4, B5 = adjust_brandx_ratings(
        b3=B3, b4=B4, b5=B5,
        brandx_in_b1=brandx_in_b1,
        is_exposed=(derived_exposed_flag==1)
    )

    # SECTION C => only if derived_exposed_flag=1
    if derived_exposed_flag==1:
        if outlier:
            # uniform suspicious pattern
            C1, C2, C3 = 1, 3, 1
            C4 = 3
            c5_list = [3,3,3,3,3,3]
            C5 = ", ".join(map(str, c5_list))
            C6 = "Average ad. Not much to say."
            C7 = np.random.choice([1,2,3,4,5,6,7])
        else:
            # Ad recall correlates with channel freq
            freq_check = (TV_Channel_A in [1,2]) or (TV_Channel_B in [1,2])
            if freq_check:
                C1 = np.random.choice([1,2,3], p=[0.80,0.15,0.05])
            else:
                C1 = np.random.choice([1,2,3], p=[0.60,0.30,0.10])

            if C1==1:
                C3 = 1
                C2 = np.random.choice(range(1,10))  # random "source code"
            else:
                C3 = np.random.choice([1,2,3], p=[0.30,0.50,0.20])
                C2 = np.nan

            # C4 => if B4≥4 or C1=1 => more positive
            if B4>=4 or C1==1:
                C4 = np.random.choice([1,2,3,4,5], p=[0.02,0.08,0.15,0.30,0.45])
            else:
                C4 = np.random.choice([1,2,3,4,5], p=[0.05,0.15,0.25,0.35,0.20])

            # C5 => 6 Likert items. If C4≥4 => nudge them up
            c5_list = [simulate_attitude() for _ in range(6)]
            if C4>=4:
                for i in range(len(c5_list)):
                    if c5_list[i]<5 and np.random.rand()<0.6:
                        c5_list[i] += 1
            C5 = ", ".join(map(str,c5_list))

            # C6 => open-ended: more positive if C4≥4
            if C4>=4:
                if np.random.rand()<0.5:
                    C6 = np.random.choice(C6_RESPONSES_POSITIVE)
                else:
                    C6 = np.random.choice(C6_RESPONSES_LONGER)
            else:
                C6 = np.random.choice(C6_RESPONSES_NEUTRAL_NEG)

            # C7 => "key message aided"
            C7 = np.random.choice([1,2,3,4,5,6,7],
                                  p=[0.50,0.10,0.10,0.05,0.10,0.10,0.05])
    else:
        # Control => no ad questions
        C1 = C2 = C3 = C4 = np.nan
        C5 = C6 = C7 = np.nan

    # SECTION D => LIFESTYLE & DEMOGRAPHICS
    # We'll nudge D2/D3 if D1=1 (primary shopper) or D7=1 (has children).
    D1 = np.random.choice([1,2,3], p=[0.70,0.25,0.05])  # 1=Primary,2=Shared,3=None
    base_d2 = np.random.choice([1,2,3,4,5,6], p=[0.10,0.40,0.20,0.15,0.10,0.05])
    base_d3 = np.random.choice([1,2,3,4,5,6], p=[0.40,0.30,0.10,0.10,0.05,0.05])

    D7 = np.random.choice([1,2], p=[0.50,0.50])
    if D7==1:
        n_kids = np.random.choice([1,2,3], p=[0.5,0.3,0.2])
        kids_ages = np.random.choice([1,2,3,4], size=n_kids, replace=False)
        D8 = ", ".join(map(str, sorted(kids_ages)))
    else:
        D8 = np.nan

    # Nudges for D2 (snack purchase freq) & D3 (weekly snack spend)
    if D1==1 and np.random.rand()<0.5:
        base_d2 = np.random.choice([1,2])
    if D1==1 and np.random.rand()<0.5:
        base_d3 = np.random.choice([1,2])

    if D7==1 and np.random.rand()<0.3:
        base_d2 = np.random.choice([1,2])
    if D7==1 and np.random.rand()<0.3:
        base_d3 = np.random.choice([1,2])

    D2 = base_d2
    D3 = base_d3

    D4 = np.random.choice([1,2,3,4,5,6,7,8], p=[0.50,0.10,0.05,0.05,0.15,0.10,0.03,0.02])
    D5 = np.random.choice([1,2,3,4,5], p=[0.30,0.30,0.30,0.08,0.02])
    D6 = np.random.choice([1,2,3,4,5], p=[0.35,0.50,0.10,0.03,0.02])
    D9 = pick_community_type()
    D10 = np.random.choice([1,2,3,4,5,6,7], p=[0.20,0.25,0.20,0.15,0.10,0.05,0.05])

    # Completion time
    comp_time = simulate_completion_time(is_outlier=outlier)

    # Build final dict
    respondent = {
        "respondent_id": resp_id,
        "Completed": 1,
        "Termination_Point": "Completed",
        "A1_purchased_snack": A1,
        "A2_gender": A2,
        "A3_age": A3,
        "A4_province": A4,
        "TV_Channel_A": TV_Channel_A,
        "TV_Channel_B": TV_Channel_B,
        "TV_Channel_C": TV_Channel_C,
        "TV_Channel_D": TV_Channel_D,
        "TV_Channel_E": TV_Channel_E,
        "A6_PotatoChips": snacks[0],
        "A6_Popcorn": snacks[1],
        "A6_Pretzels": snacks[2],
        "A6_Chocolate": snacks[3],
        "A6_GranolaBars": snacks[4],
        "A6_FruitSlices": snacks[5],
        # Derived Exposed Flag
        "Exposed_Flag": derived_exposed_flag,
        "B1_Unaided_BrandAwareness": B1,
        "B2_Aided_BrandAwareness": B2,
        "B2a_Overall_Impression": B2a,
        "B3_Familiarity_BrandX": B3,
        "B4_Consideration_BrandX": B4,
        "B5_Recommendation_BrandX": B5,
        "C1_Ad_Recall_Pre": C1,
        "C2_Ad_Source": C2,
        "C3_Ad_Recall_Post": C3,
        "C4_Ad_Enjoyment": C4,
        "C5_Ad_Attitudes": C5,
        "C6_Key_Message_Unaided": C6,
        "C7_Key_Message_Aided": C7,
        "D1_Grocery_Shopper_Role": D1,
        "D2_Snack_Purchase_Frequency": D2,
        "D3_Weekly_Snack_Spend": D3,
        "D4_Employment_Status": D4,
        "D5_Education_Level": D5,
        "D6_Marital_Status": D6,
        "D7_Children": D7,
        "D8_Children_Age": D8,
        "D9_Community_Type": D9,
        "D10_Household_Income": D10,
        "Completion_Time": comp_time
    }
    return respondent

# -----------------------------------------------------------------------------
# FINAL DATASET BUILD FUNCTION
# -----------------------------------------------------------------------------
def generate_dataset():
    """
    We want exactly:
      - 500 'complete' respondents in the EXPOSED group (Channel A<5 or B<5)
      - 500 'complete' respondents in the CONTROL group (Channel A=5 & B=5)
      - 15 outliers (some forced-exposed, some forced-control)
      - 50 terminated
    => total = 1065
    """
    # 1) 500 Exposed completes
    exposed_completes = [
        simulate_complete_respondent(
            resp_id=i,
            force_exposed=True,
            force_control=False,
            outlier=False
        )
        for i in range(1,501)
    ]
    # 2) 500 Control completes
    control_completes = [
        simulate_complete_respondent(
            resp_id=500+i,
            force_exposed=False,
            force_control=True,
            outlier=False
        )
        for i in range(1,501)
    ]

    # 3) 15 Outliers => forcibly produce suspicious patterns & extremes
    # We'll do ~ half exposed, ~ half control
    outliers = []
    n_exp_out = 8  # 8 outliers with Channel A<5 or B<5
    n_ctl_out = 7  # 7 outliers with Channel A=5 AND B=5
    base_out_id = 2000
    for i in range(n_exp_out):
        rid = base_out_id + i + 1
        outliers.append(
            simulate_complete_respondent(
                resp_id=rid,
                force_exposed=True,
                force_control=False,
                outlier=True
            )
        )
    for i in range(n_ctl_out):
        rid = base_out_id + n_exp_out + i + 1
        outliers.append(
            simulate_complete_respondent(
                resp_id=rid,
                force_exposed=False,
                force_control=True,
                outlier=True
            )
        )

    # 4) 50 terminated respondents
    # For these we do not force channel logic.
    # We'll ID them from 3001..3050
    terminated = []
    for i in range(50):
        rid = 3000 + i + 1
        terminated.append(simulate_terminated_respondent(rid))

    # Combine all
    all_respondents = exposed_completes + control_completes + outliers + terminated
    df = pd.DataFrame(all_respondents)
    # Shuffle
    df = df.sample(frac=1, random_state=123).reset_index(drop=True)

    return df

# -----------------------------------------------------------------------------
# MAIN SCRIPT
# -----------------------------------------------------------------------------
if __name__=="__main__":
    df = generate_dataset()
    print("Total respondents:", df.shape[0])  # Should be 1065

    # Quick Stats:
    completes = df[df['Completed']==1]
    n_exposed = (completes['Exposed_Flag']==1).sum()
    n_control = (completes['Exposed_Flag']==0).sum()
    print(f"Complete respondents: {len(completes)}")
    print(f"Exposed completes: {n_exposed}")
    print(f"Control completes: {n_control}")
    print(f"Terminated respondents: {len(df[df['Completed']==0])}")

    # Save to CSV
    df.to_csv("simulated_brandX_survey_dataset.csv", index=False)
    print("Dataset saved as 'simulated_brandX_survey_dataset.csv'.")
