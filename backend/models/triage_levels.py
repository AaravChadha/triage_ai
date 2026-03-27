from enum import IntEnum


class TriageLevel(IntEnum):
    EMERGENCY = 0   # Call 911
    ER = 1          # Emergency Room
    URGENT_CARE = 2 # Urgent Care
    PRIMARY = 3     # Primary Care
    TELEHEALTH = 4  # Telehealth
    SELF_CARE = 5   # Self-Care


TIER_CAPABILITIES = {
    TriageLevel.EMERGENCY: [],  # bypass — call 911, no facility needed
    TriageLevel.ER: ["trauma care", "imaging", "surgery", "ICU"],
    TriageLevel.URGENT_CARE: ["X-ray", "stitches", "IV fluids", "basic labs"],
    TriageLevel.PRIMARY: ["general consultation", "prescriptions", "referrals"],
    TriageLevel.TELEHEALTH: ["video consult", "e-prescriptions"],
    TriageLevel.SELF_CARE: [],  # no facility needed
}


TIER_LABELS = {
    TriageLevel.EMERGENCY: "Call 911",
    TriageLevel.ER: "Emergency Room",
    TriageLevel.URGENT_CARE: "Urgent Care",
    TriageLevel.PRIMARY: "Primary Care",
    TriageLevel.TELEHEALTH: "Telehealth",
    TriageLevel.SELF_CARE: "Self-Care",
}
