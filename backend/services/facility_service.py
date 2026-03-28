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

def get_nearby_facilities(triage_level: int, lat: float, lng: float, required_capabilities: list[str] = None):
    if required_capabilities is None:
        required_capabilities = []
        
    eligible = []
    
    for f in MOCK_FACILITIES:
        # 3.1.4 Filter by capabilities (must have all required)
        missing = [cap for cap in required_capabilities if cap not in f["capabilities"]]
        if missing:
            continue
            
        # 3.1.7 Enforce care level floor
        # Levels 1-2 are emergencies/high urgency -> MUST go to Tier 1 or 2
        if triage_level in (1, 2) and f["tier"] > 2:
            continue
            
        # 3.1.6 Attach mock wait times based on facility tier
        wait_time_mins = 0
        if f["tier"] == 1:
            wait_time_mins = random.randint(45, 120)
        elif f["tier"] == 2:
            wait_time_mins = random.randint(15, 45)
        elif f["tier"] == 3:
            wait_time_mins = 1440  # Mock "Next appt: tomorrow" as 24 hours
        elif f["tier"] == 4:
            wait_time_mins = random.randint(0, 5)
            
        # Format the wait time nicely
        wait_text = f"~{wait_time_mins} min wait"
        if wait_time_mins >= 1440:
            wait_text = "Next appt: tomorrow"
        elif f["tier"] == 4 and wait_time_mins == 0:
            wait_text = "Available now"
            
        # 3.1.3 Facility type is implicitly returned in the response format
        eligible.append({
            "name": f["name"],
            "address": f["address"],
            "distance_miles": f["distance"], 
            "is_open": True,  # Mocking as always open for hackathon
            "wait_time": wait_text,
            "wait_time_mins": wait_time_mins,
            "maps_url": f"https://www.google.com/maps/dir/?api=1&destination={f['address'].replace(' ', '+')}"
        })
        
    # 3.1.8 Sort by wait time ascending
    eligible.sort(key=lambda x: x["wait_time_mins"])
    
    # 3.1.5 Return top 3 results
    top_3 = eligible[:3]
    
    for i, fac in enumerate(top_3):
        fac["is_recommended"] = (i == 0)  # Top result is recommended
        del fac["wait_time_mins"]  # Remove internal sorting field
        
    return top_3
