import re

NIGERIA_PLATE_PATTERN = r"^[A-Z]{3}-?\d{3,4}[A-Z]{2}$"

LGA_STATE_MAP = {
    # Lagos
    "AAA": "LAGOS", "KJA": "LAGOS", "LSR": "LAGOS", "FST": "LAGOS",
    "IKJ": "LAGOS", "MUS": "LAGOS", "EPE": "LAGOS", "BDG": "LAGOS",
    "AKD": "LAGOS", "APP": "LAGOS", "SMK": "LAGOS", "JJJ": "LAGOS",
    "FKJ": "LAGOS", "LND": "LAGOS", "KTU": "LAGOS", "EKY": "LAGOS",
    "KRD": "LAGOS", "GGE": "LAGOS", "LSD": "LAGOS", "KSF": "LAGOS",
    "AGL": "LAGOS",

    # FCT Abuja
    "ABJ": "FCT ABUJA", "ABC": "FCT ABUJA", "GWA": "FCT ABUJA",
    "BWR": "FCT ABUJA", "KUJ": "FCT ABUJA", "KWL": "FCT ABUJA", 
    "YAB": "FCT ABUJA",


    # Rivers
    "PHC": "RIVERS", "OBK": "RIVERS", "DEG": "RIVERS",
    "ABU": "RIVERS", "ABM": "RIVERS", "OMC": "RIVERS",

    # Oyo
    "IBD": "OYO", "OYO": "OYO",

    # Kano
    "KND": "KANO", "FGE": "KANO", "GZW": "KANO",

    # Kaduna
    "KAF": "KADUNA", "ZAK": "KADUNA",

    # Delta
    "WAR": "DELTA", "ASB": "DELTA", "SAP": "DELTA",

    # Others
    "BEN": "EDO",
    "ENU": "ENUGU",
    "AWK": "ANAMBRA", "ONI": "ANAMBRA",
    "UYO": "AKWA IBOM",
    "UMU": "ABIA", "ABA": "ABIA",
    "ABK": "OGUN", "SGR": "OGUN", "ABE": "OGUN",
    "ILR": "KWARA",
    "JOS": "PLATEAU",
    "LKJ": "KOGI",
    "LAF": "NASARAWA", "DHA": "NASARAWA",
    "ADO": "EKITI",
    "AKR": "ONDO",
    "OSG": "OSUN",
    "MNA": "NIGER",
    "SKT": "SOKOTO",
    "DAM": "YOBE",
    "BAU": "BAUCHI",
    "MAI": "BORNO",
}

STATE_SLOGAN_MAP = {
    "LAGOS": "CENTRE OF EXCELLENCE",
    "FCT ABUJA": "CENTRE OF UNITY",
    "ABUJA": "CENTRE OF UNITY",
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
    "YOBE": "PRIDE OF THE SAHEL",
    "BAUCHI": "PEARL OF TOURISM",
    "BORNO": "HOME OF PEACE",
}

STATE_ALIASES = {
    "ABUJA": "FCT ABUJA",
    "FCT": "FCT ABUJA",
    "FCT ABUJA": "FCT ABUJA",
}