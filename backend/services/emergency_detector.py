EMERGENCY_PATTERNS = [
    # Cardiac
    "chest pain",
    "chest tightness",
    "heart attack",
    "cardiac arrest",

    # Stroke
    "can't move my arm",
    "can't move my leg",
    "face drooping",
    "slurred speech",
    "sudden numbness",
    "stroke",

    # Breathing
    "can't breathe",
    "not breathing",
    "stopped breathing",
    "choking",
    "shortness of breath",

    # Severe bleeding
    "won't stop bleeding",
    "bleeding heavily",
    "severe bleeding",
    "lost a lot of blood",

    # Consciousness
    "unconscious",
    "unresponsive",
    "passed out",
    "not waking up",
    "seizure",
    "convulsions",

    # Allergic reaction
    "anaphylaxis",
    "throat swelling",
    "tongue swelling",
    "can't swallow",
    "allergic reaction",

    # Other
    "overdose",
    "poisoning",
    "suicidal",
    "gunshot",
    "stabbed",
]


def check_emergency(message: str) -> bool:
    text = message.lower()
    return any(pattern in text for pattern in EMERGENCY_PATTERNS)
