# Single keywords/phrases that are almost always emergencies on their own
EMERGENCY_PATTERNS = [
    # Cardiac
    "heart attack",
    "cardiac arrest",

    # Stroke
    "face drooping",
    "slurred speech",
    "stroke",

    # Breathing — only clearly severe ones
    "not breathing",
    "stopped breathing",
    "choking",

    # Severe bleeding
    "won't stop bleeding",
    "bleeding heavily",
    "severe bleeding",
    "lost a lot of blood",

    # Consciousness
    "unconscious",
    "unresponsive",
    "not waking up",
    "seizure",
    "convulsions",

    # Allergic reaction — severe
    "anaphylaxis",
    "throat swelling",
    "tongue swelling",

    # Other
    "overdose",
    "poisoning",
    "suicidal",
    "gunshot",
    "stabbed",
]

# Combinations — only flag emergency if BOTH items appear in the message
# (individually these can be minor, together they're serious)
EMERGENCY_COMBINATIONS = [
    ("chest pain", "shortness of breath"),
    ("chest pain", "can't breathe"),
    ("chest tightness", "shortness of breath"),
    ("chest tightness", "can't breathe"),
    ("chest pain", "arm pain"),
    ("chest pain", "jaw pain"),
    ("allergic reaction", "can't breathe"),
    ("allergic reaction", "swelling"),
    ("sudden numbness", "can't move"),
    ("passed out", "chest pain"),
    ("passed out", "hit my head"),
]


def check_emergency(message: str) -> bool:
    text = message.lower()

    if any(pattern in text for pattern in EMERGENCY_PATTERNS):
        return True

    if any(a in text and b in text for a, b in EMERGENCY_COMBINATIONS):
        return True

    return False
