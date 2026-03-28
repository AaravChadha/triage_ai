import random

# Mock real-world facilities near Purdue Indianapolis campus
# Tiers: 1 = ER, 2 = Urgent Care, 3 = Primary Care, 4 = Telehealth
MOCK_FACILITIES = [
    {
        "id": "er_1",
        "name": "IU Health Methodist Hospital Emergency Room",
        "address": "1701 N Senate Ave, Indianapolis, IN 46202",
        "distance": 1.2,
        "tier": 1,
        "capabilities": ["trauma care", "imaging", "surgery", "ICU", "X-ray", "stitches", "IV fluids", "basic labs", "general consultation", "prescriptions"],
    },
    {
        "id": "er_2",
        "name": "Ascension St. Vincent Hospital - Indianapolis ER",
        "address": "2001 W 86th St, Indianapolis, IN 46260",
        "distance": 8.5,
        "tier": 1,
        "capabilities": ["trauma care", "imaging", "surgery", "ICU", "X-ray", "stitches", "IV fluids", "basic labs", "general consultation", "prescriptions"],
    },
    {
        "id": "uc_1",
        "name": "Concentra Urgent Care",
        "address": "5940 W Raymond St, Indianapolis, IN 46241",
        "distance": 4.1,
        "tier": 2,
        "capabilities": ["X-ray", "stitches", "IV fluids", "basic labs", "general consultation", "prescriptions"],
    },
    {
        "id": "uc_2",
        "name": "MedCheck CityWay",
        "address": "315 S Delaware St, Indianapolis, IN 46204",
        "distance": 1.5,
        "tier": 2,
        "capabilities": ["X-ray", "stitches", "IV fluids", "basic labs", "general consultation", "prescriptions"],
    },
    {
        "id": "pc_1",
        "name": "IU Health Primary Care Center",
        "address": "550 N University Blvd, Indianapolis, IN 46202",
        "distance": 0.5,
        "tier": 3,
        "capabilities": ["general consultation", "prescriptions", "referrals", "basic labs"],
    },
    {
        "id": "pc_2",
        "name": "Eskenazi Health Center Primary Care",
        "address": "720 Eskenazi Ave, Indianapolis, IN 46202",
        "distance": 0.8,
        "tier": 3,
        "capabilities": ["general consultation", "prescriptions", "referrals", "basic labs"],
    },
    {
        "id": "th_1",
        "name": "Purdue Student Health Telehealth",
        "address": "Virtual",
        "distance": 0.0,
        "tier": 4,
        "capabilities": ["video consult", "e-prescriptions", "general consultation"],
    },
    {
        "id": "th_2",
        "name": "Teladoc Health (Indiana)",
        "address": "Virtual",
        "distance": 0.0,
        "tier": 4,
        "capabilities": ["video consult", "e-prescriptions", "general consultation"],
    }
]

def get_nearby_facilities(triage_level: int, lat: float, lng: float, required_capabilities: list[str]) -> list:
    pass
