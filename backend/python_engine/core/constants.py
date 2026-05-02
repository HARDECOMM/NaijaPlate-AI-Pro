import re

# -----------------------------
# Nigerian Plate Format
# -----------------------------
NIGERIA_PLATE_PATTERN = r'^[A-Z]{3}-?\d{3,4}[A-Z]{2}$'


# -----------------------------
# LGA PREFIX → STATE MAP (CLEANED)
# ONLY VALID 3-LETTER PREFIXES
# -----------------------------
LGA_STATE_MAP = {

    # Lagos
    "AAA": "LAGOS", "KJA": "LAGOS", "LSR": "LAGOS", "FST": "LAGOS",
    "IKJ": "LAGOS", "MUS": "LAGOS", "EPE": "LAGOS", "BDG": "LAGOS",
    "YAB": "LAGOS", "AKD": "LAGOS",

    # FCT Abuja
    "ABJ": "FCT ABUJA", "ABC": "FCT ABUJA", "GWA": "FCT ABUJA",
    "KWA": "FCT ABUJA", "BWU": "FCT ABUJA",

    # Rivers
    "PHC": "RIVERS", "OBK": "RIVERS", "DEG": "RIVERS",

    # Oyo
    "IBD": "OYO", "OYO": "OYO",

    # Kano
    "KND": "KANO", "FGE": "KANO", "GZW": "KANO",

    # Kaduna
    "KAF": "KADUNA", "ZAK": "KADUNA",

    # Delta
    "WAR": "DELTA", "ASB": "DELTA",

    # Edo
    "BEN": "EDO",

    # Enugu
    "ENU": "ENUGU",

    # Anambra
    "AWK": "ANAMBRA", "ONI": "ANAMBRA",

    # Akwa Ibom
    "UYO": "AKWA IBOM",

    # Abia
    "UMU": "ABIA", "ABA": "ABIA",

    # Ogun
    "ABK": "OGUN", "SGR": "OGUN",

    # Kwara
    "ILR": "KWARA",

    # Plateau
    "JOS": "PLATEAU",

    # Kogi
    "LKJ": "KOGI",

    # Nasarawa
    "LAF": "NASARAWA", "DHA": "NASARAWA",

    # Others
    "ADO": "EKITI",
    "AKR": "ONDO",
    "OSG": "OSUN",
    "MNA": "NIGER",
    "SKT": "SOKOTO",
    "DAM": "YOBE",
    "BAU": "BAUCHI",
    "MAI": "BORNO",
}


# -----------------------------
# SAFE OCR FIXES (IMPORTANT FIX)
# ONLY FOR NUMERIC CONTEXT, NOT PREFIXES
# -----------------------------
OCR_DIGIT_FIXES = {
    'O': '0',
    'I': '1',
    'Z': '2',
    'S': '5',
    'B': '8',
    'G': '6'
}


# -----------------------------
# STATE SLOGANS
# -----------------------------
STATE_SLOGAN_MAP = {
    "LAGOS": "CENTRE OF EXCELLENCE",
    "FCT ABUJA": "CENTRE OF UNITY",
    "RIVERS": "TREASURE BASE OF THE NATION",
    "OYO": "PACESETTER STATE",
    "KANO": "CENTRE OF COMMERCE",
    "KADUNA": "LIBERAL STATE",
    "DELTA": "THE BIG HEART",
    "EDO": "HEARTBEAT OF THE NATION",
    "ENUGU": "COAL CITY STATE",
    "ANAMBRA": "LIGHT OF THE NATION",
    "AKWA IBOM": "LAND OF PROMISE",
    "ABIA": "GOD'S OWN STATE",
    "OGUN": "GATEWAY STATE",
    "KWARA": "STATE OF HARMONY",
    "PLATEAU": "HOME OF PEACE AND TOURISM",
    "KOGI": "THE CONFLUENCE STATE",
    "EKITI": "LAND OF HONOUR AND INTEGRITY",
    "ONDO": "SUNSHINE STATE",
    "OSUN": "LAND OF VIRTUE",
    "BENUE": "FOOD BASKET OF THE NATION",
    "NASARAWA": "HOME OF SOLID MINERALS",
    "NIGER": "THE POWER STATE",
    "SOKOTO": "SEAT OF THE CALIPHATE",
    "TARABA": "NATURE'S GIFT TO THE NATION",
    "YOBE": "PRIDE OF THE SAHEL",
    "BAUCHI": "PEARL OF TOURISM",
    "BORNO": "HOME OF PEACE",
}