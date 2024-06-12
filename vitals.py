import re
import spacy

# Load the larger spaCy model (make sure you have it installed)
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    print("Warning: Large spaCy model 'en_core_web_lg' not found. Using 'en_core_web_md' instead.")
    nlp = spacy.load("en_core_web_md")


def extract_vitals(text):
    """Extracts heart rate, blood pressure, and temperature from medical text."""

    vitals = {'heart_rate': None, 'blood_pressure': None, 'temperature': None}
    doc = nlp(text)

    # Enhanced blood pressure extraction
    bp_patterns = [
        r"(\d+) ?/ ?(\d+) (?:mm ?hg|hg/mm|millimeters of mercury|mercury)",
        r"(?:systolic|diastolic) (\d+) (?:over|mmHg)",
        r"bp (\d+ ?/ ?\d+)",
        r"(?:blood ?pressure|bp) (?:is|was|of) (\d+ ?/ ?\d+)",
        r"(?:my|his|her|the patient's) (?:blood ?pressure|bp) (?:is|was) (\d+)(?: and| over) (\d+)",
        r"(\d+) ?(?:over|/) ?(\d+)",
        r"bp is (\d+) (\d+)"
    ]
    for pattern in bp_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if len(match.groups()) == 2:
                vitals['blood_pressure'] = f"{match.group(1)}/{match.group(2)}"
            else:
                vitals['blood_pressure'] = match.group(1)
            break

    # Enhanced heart rate extraction (including "rate" keyword)
    heart_rate_patterns = [
        r"(\d+) (bpm|beats per minute|beats/minute|heartrate|rate)",
        r"heart rate (\d+)"
    ]
    for pattern in heart_rate_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            vitals['heart_rate'] = int(match.group(1))
            break

    # Enhanced temperature extraction
    temp_patterns = [
        r"(\d+(?:\.\d+)?) (?:degrees )?c",  # Celsius
        r"(\d+(?:\.\d+)?) (?:degrees )?f",  # Fahrenheit
        r"(?:temp|temperature) (?:is|was|of) (\d+(?:\.\d+)?)",
        r"(\d+(?:\.\d+)?) (?:degrees|deg|°)(?:c|f)",  # More flexible degree symbol
        r"fever of (\d+(?:\.\d+)?)",
    ]
    for pattern in temp_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            temp_value = float(match.group(1))
            if "f" in pattern.lower() or "fever" in pattern.lower():
                temp_value = (temp_value - 32) * 5 / 9  # Convert to Celsius
            vitals['temperature'] = round(temp_value, 1)
            break

    return vitals


# Main loop for user input (or use in your medical recommendation system)
while True:
    text = input("Enter medical text (or type 'quit' to exit): ")

    if text.lower() == "quit":
        break

    vitals = extract_vitals(text)
    if any(vitals.values()):
        print(f"Vitals extracted from text: {vitals}")
    else:
        print("No vitals found in the text.")

test_cases = [
    "Patient presents with a temperature of 38.5 degrees Celsius, a heart rate of 100 bpm, and blood pressure of 130/85 mm Hg.",
    "The patient's blood pressure is 120/80 mm Hg, and their heartrate is 85 beats per minute. No fever noted.",
    "Temp: 98.6 F, BP: 118/78, HR: 72",
    "hello my name is doctor rosh. patient name is rahul gandhi how can we. the temprature of the human subject is 105 degree ferhenite and a and bloos pressure is 120 88",
    "y blood pressure is 120 80",
    "bp is 120 80",
    "my name is anushi mangal and my age is 40 years i am suffering from fever. doctor says temprature is 105 degree and rate is 77 bpm with bp as 200 over 100"
]

for text in test_cases:
    vitals = extract_vitals(text)
    print(f"Text: '{text}'\nVitals: {vitals}\n")
